# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging
import subprocess
import threading
import time

from openstack import exceptions as sdk_exc
from oslo_utils import strutils
import six

from senlinclient.common import exc
from senlinclient.common.i18n import _
from senlinclient.common import utils

logger = logging.getLogger(__name__)


def show_deprecated(deprecated, recommended):
    logger.warning(
        ('"%(old)s" is deprecated and will be removed by Apr 2017, '
         'please use "%(new)s" instead.'),
        {'old': deprecated, 'new': recommended})


def do_build_info(service, args=None):
    """Retrieve build information."""
    show_deprecated('senlin build-info', 'openstack cluster build info')
    result = service.get_build_info()
    info = {'api': result.api, 'engine': result.engine}

    formatters = {
        'api': utils.json_formatter,
        'engine': utils.json_formatter,
    }
    utils.print_dict(info, formatters=formatters)


# PROFILE TYPES

def do_profile_type_list(service, args=None):
    """List the available profile types."""
    show_deprecated('senlin profile-type-list',
                    'openstack cluster profile type list')

    class _ProfileType(object):

        def __init__(self, name, version, status):
            self.name = name
            self.version = version
            self.support_status = status

    fields = ['name', 'version', 'support_status']
    types = service.profile_types()
    results = []
    for t in types:
        for v in t.support_status.keys():
            ss = '\n'.join([' since '.join((item['status'], item['since']))
                           for item in t.support_status[v]])
            results.append(_ProfileType(t.name, v, ss))

    utils.print_list(results, fields, sortby_index=0)


@utils.arg('type_name', metavar='<TYPE_NAME>',
           help=_('Profile type to retrieve.'))
@utils.arg('-F', '--format', metavar='<FORMAT>',
           choices=utils.supported_formats.keys(),
           help=_("The template output format, one of: %s.")
                 % ', '.join(utils.supported_formats.keys()))
def do_profile_type_show(service, args):
    """Get the details about a profile type."""
    show_deprecated('senlin profile-type-show',
                    'openstack cluster profile type show')
    try:
        res = service.get_profile_type(args.type_name)
    except sdk_exc.ResourceNotFound:
        raise exc.CommandError(
            _('Profile Type not found: %s') % args.type_name)

    pt = res.to_dict()

    if args.format:
        print(utils.format_output(pt, format=args.format))
    else:
        print(utils.format_output(pt))


# PROFILES

@utils.arg('-f', '--filters', metavar='<"KEY1=VALUE1;KEY2=VALUE2...">',
           help=_('Filter parameters to apply on returned profiles. '
                  'This can be specified multiple times, or once with '
                  'parameters separated by a semicolon.'),
           action='append')
@utils.arg('-l', '--limit', metavar='<LIMIT>',
           help=_('Limit the number of profiles returned.'))
@utils.arg('-m', '--marker', metavar='<ID>',
           help=_('Only return profiles that appear after the given ID.'))
@utils.arg('-o', '--sort', metavar='<KEY:DIR>',
           help=_('Sorting option which is a string containing a list of keys '
                  'separated by commas. Each key can be optionally appended '
                  'by a sort direction (:asc or :desc)'))
@utils.arg('-g', '--global-project', default=False, action="store_true",
           help=_('Indicate that the list should include profiles from'
                  ' all projects. This option is subject to access policy '
                  'checking. Default is False.'))
@utils.arg('-F', '--full-id', default=False, action="store_true",
           help=_('Print full IDs in list.'))
def do_profile_list(service, args=None):
    """List profiles that meet the criteria."""
    show_deprecated('senlin profile-list', 'openstack cluster profile list')
    fields = ['id', 'name', 'type', 'created_at']
    queries = {
        'limit': args.limit,
        'marker': args.marker,
        'sort': args.sort,
        'global_project': args.global_project,
    }
    if args.filters:
        queries.update(utils.format_parameters(args.filters))

    sortby_index = None if args.sort else 1

    profiles = service.profiles(**queries)
    formatters = {}
    if args.global_project:
        fields.append('project_id')
    if not args.full_id:
        formatters = {
            'id': lambda x: x.id[:8],
        }
        if 'project_id' in fields:
            formatters['project_id'] = lambda x: x.project_id[:8]

    utils.print_list(profiles, fields, formatters=formatters,
                     sortby_index=sortby_index)


def _show_profile(service, profile_id):
    try:
        profile = service.get_profile(profile_id)
    except sdk_exc.ResourceNotFound:
        raise exc.CommandError(_('Profile not found: %s') % profile_id)

    formatters = {
        'metadata': utils.json_formatter,
    }

    formatters['spec'] = utils.nested_dict_formatter(
        ['type', 'version', 'properties'],
        ['property', 'value'])

    utils.print_dict(profile.to_dict(), formatters=formatters)


@utils.arg('-s', '--spec-file', metavar='<SPEC FILE>', required=True,
           help=_('The spec file used to create the profile.'))
@utils.arg('-M', '--metadata', metavar='<"KEY1=VALUE1;KEY2=VALUE2...">',
           help=_('Metadata values to be attached to the profile. '
                  'This can be specified multiple times, or once with '
                  'key-value pairs separated by a semicolon.'),
           action='append')
@utils.arg('name', metavar='<PROFILE_NAME>',
           help=_('Name of the profile to create.'))
def do_profile_create(service, args):
    """Create a profile."""
    show_deprecated('senlin profile-create',
                    'openstack cluster profile create')
    spec = utils.get_spec_content(args.spec_file)
    type_name = spec.get('type', None)
    type_version = spec.get('version', None)
    properties = spec.get('properties', None)
    if type_name is None:
        raise exc.CommandError(_("Missing 'type' key in spec file."))
    if type_version is None:
        raise exc.CommandError(_("Missing 'version' key in spec file."))
    if properties is None:
        raise exc.CommandError(_("Missing 'properties' key in spec file."))

    if type_name == 'os.heat.stack':
        stack_properties = utils.process_stack_spec(properties)
        spec['properties'] = stack_properties

    params = {
        'name': args.name,
        'spec': spec,
        'metadata': utils.format_parameters(args.metadata),
    }

    profile = service.create_profile(**params)
    _show_profile(service, profile.id)


@utils.arg('id', metavar='<PROFILE>',
           help=_('Name or ID of profile to show.'))
def do_profile_show(service, args):
    """Show the profile details."""
    show_deprecated('senlin profile-show', 'openstack cluster profile show')
    _show_profile(service, args.id)


@utils.arg('-n', '--name', metavar='<NAME>',
           help=_('The new name for the profile.'))
@utils.arg('-M', '--metadata', metavar='<"KEY1=VALUE1;KEY2=VALUE2...">',
           help=_("Metadata values to be attached to the profile. "
                  "This can be specified multiple times, or once with "
                  "key-value pairs separated by a semicolon. Use '{}' "
                  "can clean metadata "),
           action='append')
@utils.arg('id', metavar='<PROFILE_ID>',
           help=_('Name or ID of the profile to update.'))
def do_profile_update(service, args):
    """Update a profile."""
    show_deprecated('senlin profile-update',
                    'openstack cluster profile update')
    params = {
        'name': args.name,
    }
    if args.metadata:
        params['metadata'] = utils.format_parameters(args.metadata)

    # Find the profile first, we need its id
    try:
        profile = service.get_profile(args.id)
    except sdk_exc.ResourceNotFound:
        raise exc.CommandError(_('Profile not found: %s') % args.id)
    service.update_profile(profile, **params)
    _show_profile(service, profile.id)


@utils.arg('id', metavar='<PROFILE>', nargs='+',
           help=_('Name or ID of profile(s) to delete.'))
def do_profile_delete(service, args):
    """Delete profile(s)."""
    show_deprecated('senlin profile-delete',
                    'openstack cluster profile delete')
    failure_count = 0

    for pid in args.id:
        try:
            service.delete_profile(pid, False)
        except Exception as ex:
            failure_count += 1
            print(ex)
    if failure_count > 0:
        msg = _('Failed to delete some of the specified profile(s).')
        raise exc.CommandError(msg)
    print('Profile deleted: %s' % args.id)


@utils.arg('-s', '--spec-file', metavar='<SPEC FILE>', required=True,
           help=_('The spec file of the profile to be validated.'))
def do_profile_validate(service, args):
    """Validate a profile."""
    show_deprecated('senlin profile-validate',
                    'openstack cluster profile validate')
    spec = utils.get_spec_content(args.spec_file)
    type_name = spec.get('type', None)
    type_version = spec.get('version', None)
    properties = spec.get('properties', None)
    if type_name is None:
        raise exc.CommandError(_("Missing 'type' key in spec file."))
    if type_version is None:
        raise exc.CommandError(_("Missing 'version' key in spec file."))
    if properties is None:
        raise exc.CommandError(_("Missing 'properties' key in spec file."))

    if type_name == 'os.heat.stack':
        stack_properties = utils.process_stack_spec(properties)
        spec['properties'] = stack_properties

    params = {
        'spec': spec,
    }

    profile = service.validate_profile(**params)

    formatters = {
        'metadata': utils.json_formatter,
    }

    formatters['spec'] = utils.nested_dict_formatter(
        ['type', 'version', 'properties'],
        ['property', 'value'])

    utils.print_dict(profile.to_dict(), formatters=formatters)


# POLICY TYPES


def do_policy_type_list(service, args):
    """List the available policy types."""
    show_deprecated('senlin policy-type-list',
                    'openstack cluster policy type list')

    class _PolicyType(object):

        def __init__(self, name, version, status):
            self.name = name
            self.version = version
            self.support_status = status

    fields = ['name', 'version', 'support_status']
    types = service.policy_types()

    results = []
    for t in types:
        for v in t.support_status.keys():
            ss = '\n'.join([' since '.join((item['status'], item['since']))
                           for item in t.support_status[v]])
            results.append(_PolicyType(t.name, v, ss))

    utils.print_list(results, fields, sortby_index=0)


@utils.arg('type_name', metavar='<TYPE_NAME>',
           help=_('Policy type to retrieve.'))
@utils.arg('-F', '--format', metavar='<FORMAT>',
           choices=utils.supported_formats.keys(),
           help=_("The template output format, one of: %s.")
                 % ', '.join(utils.supported_formats.keys()))
def do_policy_type_show(service, args):
    """Get the details about a policy type."""
    show_deprecated('senlin policy-type-show',
                    'openstack cluster policy type show')
    try:
        res = service.get_policy_type(args.type_name)
    except sdk_exc.ResourceNotFound:
        raise exc.CommandError(_('Policy type not found: %s') % args.type_name)

    pt = res.to_dict()
    if args.format:
        print(utils.format_output(pt, format=args.format))
    else:
        print(utils.format_output(pt))


# POLICIES

@utils.arg('-f', '--filters', metavar='<"KEY1=VALUE1;KEY2=VALUE2...">',
           help=_('Filter parameters to apply on returned policies. '
                  'This can be specified multiple times, or once with '
                  'parameters separated by a semicolon.'),
           action='append')
@utils.arg('-l', '--limit', metavar='<LIMIT>',
           help=_('Limit the number of policies returned.'))
@utils.arg('-m', '--marker', metavar='<ID>',
           help=_('Only return policies that appear after the given ID.'))
@utils.arg('-o', '--sort', metavar='<KEY:DIR>',
           help=_('Sorting option which is a string containing a list of keys '
                  'separated by commas. Each key can be optionally appended '
                  'by a sort direction (:asc or :desc)'))
@utils.arg('-g', '--global-project', default=False, action="store_true",
           help=_('Indicate that the list should include policies from'
                  ' all projects. This option is subject to access policy '
                  'checking. Default is False.'))
@utils.arg('-F', '--full-id', default=False, action="store_true",
           help=_('Print full IDs in list.'))
def do_policy_list(service, args=None):
    """List policies that meet the criteria."""
    show_deprecated('senlin policy-list', 'openstack cluster policy list')
    fields = ['id', 'name', 'type', 'created_at']
    queries = {
        'limit': args.limit,
        'marker': args.marker,
        'sort': args.sort,
        'global_project': args.global_project,
    }
    if args.filters:
        queries.update(utils.format_parameters(args.filters))

    sortby_index = None if args.sort else 1
    policies = service.policies(**queries)
    formatters = {}
    if args.global_project:
        fields.append('project_id')
    if not args.full_id:
        formatters = {
            'id': lambda x: x.id[:8]
        }
        if 'project_id' in fields:
            formatters['project_id'] = lambda x: x.project_id[:8]

    utils.print_list(policies, fields, formatters=formatters,
                     sortby_index=sortby_index)


def _show_policy(service, policy_id):
    try:
        policy = service.get_policy(policy_id)
    except sdk_exc.ResourceNotFound:
        raise exc.CommandError(_('Policy not found: %s') % policy_id)

    formatters = {
        'metadata': utils.json_formatter,
        'spec': utils.json_formatter,
    }
    utils.print_dict(policy.to_dict(), formatters=formatters)


@utils.arg('-s', '--spec-file', metavar='<SPEC_FILE>', required=True,
           help=_('The spec file used to create the policy.'))
@utils.arg('name', metavar='<NAME>',
           help=_('Name of the policy to create.'))
def do_policy_create(service, args):
    """Create a policy."""
    show_deprecated('senlin policy-create', 'openstack cluster policy create')
    spec = utils.get_spec_content(args.spec_file)
    attrs = {
        'name': args.name,
        'spec': spec,
    }

    policy = service.create_policy(**attrs)
    _show_policy(service, policy.id)


@utils.arg('id', metavar='<POLICY>',
           help=_('Name or ID of the policy to be shown.'))
def do_policy_show(service, args):
    """Show the policy details."""
    show_deprecated('senlin policy-show', 'openstack cluster policy show')
    _show_policy(service, policy_id=args.id)


@utils.arg('-n', '--name', metavar='<NAME>',
           help=_('New name of the policy to be updated.'))
@utils.arg('id', metavar='<POLICY>',
           help=_('Name of the policy to be updated.'))
def do_policy_update(service, args):
    """Update a policy."""
    show_deprecated('senlin policy-update', 'openstack cluster policy update')
    params = {
        'name': args.name,
    }

    policy = service.get_policy(args.id)
    if policy is not None:
        service.update_policy(policy, **params)
        _show_policy(service, policy_id=policy.id)


@utils.arg('id', metavar='<POLICY>', nargs='+',
           help=_('Name or ID of policy(s) to delete.'))
def do_policy_delete(service, args):
    """Delete policy(s)."""
    show_deprecated('senlin policy-delete', 'openstack cluster policy delete')
    failure_count = 0

    for pid in args.id:
        try:
            service.delete_policy(pid, False)
        except Exception as ex:
            failure_count += 1
            print(ex)
    if failure_count > 0:
        msg = _('Failed to delete some of the specified policy(s).')
        raise exc.CommandError(msg)
    print('Policy deleted: %s' % args.id)


@utils.arg('-s', '--spec-file', metavar='<SPEC_FILE>', required=True,
           help=_('The spec file of the policy to be validated.'))
def do_policy_validate(service, args):
    """Validate a policy spec."""
    show_deprecated('senlin policy-validate',
                    'openstack cluster policy validate')
    spec = utils.get_spec_content(args.spec_file)
    attrs = {
        'spec': spec,
    }

    policy = service.validate_policy(**attrs)
    formatters = {
        'metadata': utils.json_formatter,
        'spec': utils.json_formatter,
    }
    utils.print_dict(policy.to_dict(), formatters=formatters)

# CLUSTERS


@utils.arg('-f', '--filters', metavar='<"KEY1=VALUE1;KEY2=VALUE2...">',
           help=_('Filter parameters to apply on returned clusters. '
                  'This can be specified multiple times, or once with '
                  'parameters separated by a semicolon.'),
           action='append')
@utils.arg('-o', '--sort', metavar='<KEY:DIR>',
           help=_('Sorting option which is a string containing a list of keys '
                  'separated by commas. Each key can be optionally appended '
                  'by a sort direction (:asc or :desc)'))
@utils.arg('-l', '--limit', metavar='<LIMIT>',
           help=_('Limit the number of clusters returned.'))
@utils.arg('-m', '--marker', metavar='<ID>',
           help=_('Only return clusters that appear after the given cluster '
                  'ID.'))
@utils.arg('-g', '--global-project', default=False, action="store_true",
           help=_('Indicate that the cluster list should include clusters from'
                  ' all projects. This option is subject to access policy '
                  'checking. Default is False.'))
@utils.arg('-F', '--full-id', default=False, action="store_true",
           help=_('Print full IDs in list.'))
def do_cluster_list(service, args=None):
    """List the user's clusters."""
    show_deprecated('senlin cluster-list', 'openstack cluster list')
    fields = ['id', 'name', 'status', 'created_at', 'updated_at']
    queries = {
        'limit': args.limit,
        'marker': args.marker,
        'sort': args.sort,
        'global_project': args.global_project,
    }
    if args.filters:
        queries.update(utils.format_parameters(args.filters))

    sortby_index = None if args.sort else 3

    clusters = service.clusters(**queries)
    formatters = {}
    if args.global_project:
        fields.append('project_id')
    if not args.full_id:
        formatters = {
            'id': lambda x: x.id[:8]
        }
        if 'project_id' in fields:
            formatters['project_id'] = lambda x: x.project_id[:8]

    utils.print_list(clusters, fields, formatters=formatters,
                     sortby_index=sortby_index)


def _show_cluster(service, cluster_id):
    try:
        cluster = service.get_cluster(cluster_id)
    except sdk_exc.ResourceNotFound:
        raise exc.CommandError(_('Cluster not found: %s') % cluster_id)

    formatters = {
        'config': utils.json_formatter,
        'metadata': utils.json_formatter,
        'node_ids': utils.list_formatter,
    }
    cluster_attrs = cluster.to_dict()
    cluster_attrs.pop('is_profile_only')
    utils.print_dict(cluster_attrs, formatters=formatters)


@utils.arg('-p', '--profile', metavar='<PROFILE>', required=True,
           help=_('Default profile Id or name used for this cluster.'))
@utils.arg('-n', '--min-size', metavar='<MIN-SIZE>', default=0,
           help=_('Min size of the cluster. Default to 0.'))
@utils.arg('-m', '--max-size', metavar='<MAX-SIZE>', default=-1,
           help=_('Max size of the cluster. Default to -1, means unlimited.'))
@utils.arg('-c', '--desired-capacity', metavar='<DESIRED-CAPACITY>', default=0,
           help=_('Desired capacity of the cluster. Default to min_size if '
                  'min_size is specified else 0.'))
@utils.arg('-t', '--timeout', metavar='<TIMEOUT>', type=int,
           help=_('Cluster creation timeout in seconds.'))
@utils.arg('-C', '--config', metavar='<"key1=value1;key2=value2...">',
           help=_('Configuration of the cluster. Default to {}. '
                  'This can be specified multiple times, or once with '
                  'key-value pairs separated by a semicolon.'),
           action='append')
@utils.arg('-M', '--metadata', metavar='<"KEY1=VALUE1;KEY2=VALUE2...">',
           help=_('Metadata values to be attached to the cluster. '
                  'This can be specified multiple times, or once with '
                  'key-value pairs separated by a semicolon.'),
           action='append')
@utils.arg('name', metavar='<CLUSTER_NAME>',
           help=_('Name of the cluster to create.'))
def do_cluster_create(service, args):
    """Create the cluster."""
    show_deprecated('senlin cluster-create', 'openstack cluster create')
    if args.min_size and not args.desired_capacity:
        args.desired_capacity = args.min_size
    attrs = {
        'config': utils.format_parameters(args.config),
        'name': args.name,
        'profile_id': args.profile,
        'min_size': args.min_size,
        'max_size': args.max_size,
        'desired_capacity': args.desired_capacity,
        'metadata': utils.format_parameters(args.metadata),
        'timeout': args.timeout
    }

    cluster = service.create_cluster(**attrs)
    _show_cluster(service, cluster.id)


@utils.arg('-p', '--path', metavar='<PATH>', required=True,
           help=_('A Json path string specifying the attribute to collect.'))
@utils.arg('-L', '--list', default=False, action="store_true",
           help=_('Print a full list that contains both node ids and '
                  'attribute values instead of values only. Default is '
                  'False.'))
@utils.arg('-F', '--full-id', default=False, action="store_true",
           help=_('Print full IDs in list.'))
@utils.arg('id', metavar='<CLUSTER>',
           help=_('Name or ID of cluster(s) to operate on.'))
def do_cluster_collect(service, args):
    """Collect attributes across a cluster."""
    show_deprecated('senlin cluster-collect', 'openstack cluster collect')

    attrs = service.collect_cluster_attrs(args.id, args.path)
    if args.list:
        fields = ['node_id', 'attr_value']
        formatters = {
            'attr_value': lambda x: utils.json_formatter(x.attr_value)
        }
        if not args.full_id:
            formatters['node_id'] = lambda x: x.node_id[:8]
        utils.print_list(attrs, fields, formatters=formatters)
    else:
        for attr in attrs:
            print(attr.attr_value)


@utils.arg('id', metavar='<CLUSTER>', nargs='+',
           help=_('Name or ID of cluster(s) to delete.'))
def do_cluster_delete(service, args):
    """Delete the cluster(s)."""
    show_deprecated('senlin cluster-delete', 'openstack cluster delete')

    result = {}
    for cid in args.id:
        try:
            cluster = service.delete_cluster(cid, False)
            result[cid] = ('OK', cluster.location.split('/')[-1])
        except Exception as ex:
            result[cid] = ('ERROR', six.text_type(ex))

    for rid, res in result.items():
        utils.print_action_result(rid, res)


def _run_script(node_id, addr, net, addr_type, port, user, ipv6, identity_file,
                script, options, output=None):
    version = 6 if ipv6 else 4

    # Select the network to use.
    if net:
        addresses = addr.get(net)
        if not addresses:
            output['status'] = _('FAILED')
            output['reason'] = _("Node '%(node)s' is not attached to network "
                                 "'%(net)s'.") % {'node': node_id, 'net': net}
            return
    else:
        # network not specified
        if len(addr) > 1:
            output['status'] = _('FAILED')
            output['reason'] = _("Node '%(node)s' is attached to more than "
                                 "one network. Please pick the network to "
                                 "use.") % {'node': node_id}
            return
        elif not addr:
            output['status'] = _('FAILED')
            output['reason'] = _("Node '%(node)s' is not attached to any "
                                 "network.") % {'node': node_id}
            return
        else:
            addresses = list(addr.values())[0]

    # Select the address in the selected network.
    # If the extension is not present, we assume the address to be floating.
    matching_addresses = []
    for a in addresses:
        a_type = a.get('OS-EXT-IPS:type', 'floating')
        a_version = a.get('version')
        if (a_version == version and a_type == addr_type):
            matching_addresses.append(a.get('addr'))

    if not matching_addresses:
        output['status'] = _('FAILED')
        output['reason'] = _("No address that would match network '%(net)s' "
                             "and type '%(type)s' of IPv%(ver)s has been "
                             "found for node '%(node)s'."
                             ) % {'net': net, 'type': addr_type,
                                  'ver': version, 'node': node_id}
        return

    if len(matching_addresses) > 1:
        output['status'] = _('FAILED')
        output['reason'] = _("More than one IPv%(ver)s %(type)s address "
                             "found.") % {'ver': version, 'type': addr_type}
        return

    ip_address = str(matching_addresses[0])
    identity = '-i %s' % identity_file if identity_file else ''

    cmd = [
        'ssh',
        '-%d' % version,
        '-p%d' % port,
        identity,
        options,
        '%s@%s' % (user, ip_address),
        '%s' % script
    ]
    logger.debug("%s" % cmd)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    (stdout, stderr) = proc.communicate()
    while proc.returncode is None:
        time.sleep(1)
    if proc.returncode == 0:
        output['status'] = _('SUCCEEDED (0)')
        output['output'] = stdout
        if stderr:
            output['error'] = stderr
    else:
        output['status'] = _('FAILED (%d)') % proc.returncode
        output['output'] = stdout
        if stderr:
            output['error'] = stderr


@utils.arg("-p", "--port", metavar="<PORT>", type=int, default=22,
           help=_("Optional flag to indicate the port to use (Default=22)."))
@utils.arg("-t", "--address-type", type=str, default="floating",
           help=_("Optional flag to indicate which IP type to use. Possible "
                  "values includes 'fixed' and 'floating' (the Default)."))
@utils.arg("-n", "--network", metavar='<NETWORK>', default='',
           help=_('Network to use for the ssh.'))
@utils.arg("-6", "--ipv6", action="store_true", default=False,
           help=_("Optional flag to indicate whether to use an IPv6 address "
                  "attached to a server. (Defaults to IPv4 address)"))
@utils.arg("-u", "--user", metavar="<USER>", default="root",
           help=_("Login to use."))
@utils.arg("-i", "--identity-file",
           help=_("Private key file, same as the '-i' option to the ssh "
                  "command."))
@utils.arg("-O", "--ssh-options", default="",
           help=_("Extra options to pass to ssh. see: man ssh."))
@utils.arg("-s", "--script", metavar="<FILE>", required=True,
           help=_("Script file to run."))
@utils.arg("id", metavar="<CLUSTER>",
           help=_('Name or ID of the cluster.'))
def do_cluster_run(service, args):
    """Run shell scripts on all nodes of a cluster."""
    show_deprecated('senlin cluster-run', 'openstack cluster run')

    if '@' in args.id:
        user, cluster = args.id.split('@', 1)
        args.user = user
        args.cluster = cluster

    try:
        attributes = service.collect_cluster_attrs(args.id, 'details')
    except sdk_exc.ResourceNotFound:
        raise exc.CommandError(_("Cluster not found: %s") % args.id)

    script = None
    try:
        f = open(args.script, 'r')
        script = f.read()
    except Exception:
        raise exc.CommandError(_("Cound not open script file: %s") %
                               args.script)

    tasks = dict()
    for attr in attributes:
        node_id = attr.node_id
        addr = attr.attr_value['addresses']

        output = dict()
        th = threading.Thread(
            target=_run_script,
            args=(node_id, addr, args.network, args.address_type, args.port,
                  args.user, args.ipv6, args.identity_file,
                  script, args.ssh_options),
            kwargs={'output': output})
        th.start()
        tasks[th] = (node_id, output)

    for t in tasks:
        t.join()

    for t in tasks:
        node_id, result = tasks[t]
        print("node: %s" % node_id)
        print("status: %s" % result.get('status'))
        if "reason" in result:
            print("reason: %s" % result.get('reason'))
        if "output" in result:
            print("output:\n%s" % result.get('output'))
        if "error" in result:
            print("error:\n%s" % result.get('error'))


@utils.arg('-p', '--profile', metavar='<PROFILE>',
           help=_('ID or name of new profile to use.'))
@utils.arg('-P', '--profile-only', metavar='<BOOLEAN>', default=False,
           help=_("Whether the cluster should be updated profile only. "
                  "If false, it will be applied to all existing nodes. "
                  "If true, any newly created nodes will use the new profile, "
                  "but existing nodes will not be changed. Default is False."))
@utils.arg('-t', '--timeout', metavar='<TIMEOUT>',
           help=_('New timeout (in seconds) value for the cluster.'))
@utils.arg('-C', '--config', metavar='<"key1=value1;key2=value2...">',
           help=_('Configuration of the cluster. Default to {}. '
                  'This can be specified multiple times, or once with '
                  'key-value pairs separated by a semicolon.'),
           action='append')
@utils.arg('-M', '--metadata', metavar='<"KEY1=VALUE1;KEY2=VALUE2...">',
           help=_("Metadata values to be attached to the cluster. "
                  "This can be specified multiple times, or once with "
                  "key-value pairs separated by a semicolon. Use '{}' "
                  "can clean metadata "),
           action='append')
@utils.arg('-n', '--name', metavar='<NAME>',
           help=_('New name for the cluster to update.'))
@utils.arg('id', metavar='<CLUSTER>',
           help=_('Name or ID of cluster to be updated.'))
def do_cluster_update(service, args):
    """Update the cluster."""
    show_deprecated('senlin cluster-update', 'openstack cluster update')
    cluster = service.get_cluster(args.id)
    attrs = {
        'name': args.name,
        'profile_id': args.profile,
        'profile_only': strutils.bool_from_string(
            args.profile_only, strict=True
        ),
        'metadata': utils.format_parameters(args.metadata),
        'timeout': args.timeout,
    }

    service.update_cluster(cluster, **attrs)
    _show_cluster(service, cluster.id)


@utils.arg('id', metavar='<CLUSTER>',
           help=_('Name or ID of cluster to show.'))
def do_cluster_show(service, args):
    """Show details of the cluster."""
    show_deprecated('senlin cluster-show', 'openstack cluster show')
    _show_cluster(service, args.id)


@utils.arg('-f', '--filters', metavar='<"KEY1=VALUE1;KEY2=VALUE2...">',
           help=_('Filter parameters to apply on returned nodes. '
                  'This can be specified multiple times, or once with '
                  'parameters separated by a semicolon.'),
           action='append')
@utils.arg('-l', '--limit', metavar='<LIMIT>',
           help=_('Limit the number of nodes returned.'))
@utils.arg('-m', '--marker', metavar='<ID>',
           help=_('Only return nodes that appear after the given node ID.'))
@utils.arg('-F', '--full-id', default=False, action="store_true",
           help=_('Print full IDs in list.'))
@utils.arg('id', metavar='<CLUSTER>',
           help=_('Name or ID of cluster to nodes from.'))
def do_cluster_node_list(service, args):
    """List nodes from cluster."""
    show_deprecated('senlin cluster-node-list',
                    'openstack cluster members list')
    queries = {
        'cluster_id': args.id,
        'limit': args.limit,
        'marker': args.marker,
    }
    if args.filters:
        queries.update(utils.format_parameters(args.filters))

    nodes = service.nodes(**queries)
    if not args.full_id:
        formatters = {
            'id': lambda x: x.id[:8],
            'physical_id': lambda x: x.physical_id[:8] if x.physical_id else ''
        }
    else:
        formatters = {}

    fields = ['id', 'name', 'index', 'status', 'physical_id', 'created_at']
    utils.print_list(nodes, fields, formatters=formatters, sortby_index=5)


@utils.arg('-n', '--nodes', metavar='<NODES>', required=True,
           help=_('ID of nodes to be added; multiple nodes can be separated '
                  'with ","'))
@utils.arg('id', metavar='<CLUSTER>',
           help=_('Name or ID of cluster to operate on.'))
def do_cluster_node_add(service, args):
    """Add specified nodes to cluster."""
    show_deprecated('senlin cluster-node-add',
                    'openstack cluster node members add')
    node_ids = args.nodes.split(',')
    resp = service.cluster_add_nodes(args.id, node_ids)
    print('Request accepted by action: %s' % resp['action'])


@utils.arg('-n', '--nodes', metavar='<NODES>', required=True,
           help=_('ID of nodes to be deleted; multiple nodes can be separated '
                  'with ",".'))
@utils.arg('-d', '--destroy-after-deletion', metavar='<BOOLEAN>',
           required=False, default=False,
           help=_('Whether nodes should be destroyed after deleted. '
                  'Default is False.'))
@utils.arg('id', metavar='<CLUSTER>',
           help=_('Name or ID of cluster to operate on.'))
def do_cluster_node_del(service, args):
    """Delete specified nodes from cluster."""
    show_deprecated('senlin cluster-node-del',
                    'openstack cluster node members del')
    node_ids = args.nodes.split(',')
    destroy = args.destroy_after_deletion
    destroy = strutils.bool_from_string(destroy, strict=True)
    kwargs = {"destroy_after_deletion": destroy}
    resp = service.cluster_del_nodes(args.id, node_ids, **kwargs)
    print('Request accepted by action: %s' % resp['action'])


@utils.arg('-n', '--nodes', metavar='<OLD_NODE1=NEW_NODE1>', required=True,
           help=_("OLD_NODE is the name or ID of a node to be replaced, "
                  "NEW_NODE is the name or ID of a node as replacement. "
                  "This can be specified multiple times, or once with "
                  "node-pairs separated by a comma ','."),
           action='append')
@utils.arg('id', metavar='<CLUSTER>',
           help=_('Name or ID of cluster to operate on.'))
def do_cluster_node_replace(service, args):
    """Replace the nodes in cluster with specified nodes."""
    show_deprecated('senlin cluster-node-replace',
                    'openstack cluster node members replace')
    nodepairs = {}
    for nodepair in args.nodes:
        key = nodepair.split('=')[0]
        value = nodepair.split('=')[1]
        nodepairs[key] = value
    resp = service.cluster_replace_nodes(args.id, nodepairs)
    print('Request accepted by action: %s' % resp['action'])


@utils.arg('-c', '--capacity', metavar='<CAPACITY>', type=int,
           help=_('The desired number of nodes of the cluster.'))
@utils.arg('-a', '--adjustment', metavar='<ADJUSTMENT>', type=int,
           help=_('A positive integer meaning the number of nodes to add, '
                  'or a negative integer indicating the number of nodes to '
                  'remove.'))
@utils.arg('-p', '--percentage', metavar='<PERCENTAGE>', type=float,
           help=_('A value that is interpreted as the percentage of size '
                  'adjustment. This value can be positive or negative.'))
@utils.arg('-t', '--min-step', metavar='<MIN_STEP>', type=int,
           help=_('An integer specifying the number of nodes for adjustment '
                  'when <PERCENTAGE> is specified.'))
@utils.arg('-s', '--strict', action='store_true', default=False,
           help=_('A boolean specifying whether the resize should be '
                  'performed on a best-effort basis when the new capacity '
                  'may go beyond size constraints.'))
@utils.arg('-n', '--min-size', metavar='MIN', type=int,
           help=_('New lower bound of cluster size.'))
@utils.arg('-m', '--max-size', metavar='MAX', type=int,
           help=_('New upper bound of cluster size. A value of -1 indicates '
                  'no upper limit on cluster size.'))
@utils.arg('id', metavar='<CLUSTER>',
           help=_('Name or ID of cluster to operate on.'))
def do_cluster_resize(service, args):
    """Resize a cluster."""
    # validate parameters
    # NOTE: this will be much simpler if cliutils supports exclusive groups
    show_deprecated('senlin cluster-resize', 'openstack cluster resize')
    action_args = {}

    capacity = args.capacity
    adjustment = args.adjustment
    percentage = args.percentage
    min_size = args.min_size
    max_size = args.max_size
    min_step = args.min_step

    if sum(v is not None for v in (capacity, adjustment, percentage, min_size,
                                   max_size)) == 0:
        raise exc.CommandError(_("At least one parameter of 'capacity', "
                                 "'adjustment', 'percentage', 'min_size', "
                                 " and 'max_size' should be specified."))

    if sum(v is not None for v in (capacity, adjustment, percentage)) > 1:
        raise exc.CommandError(_("Only one of 'capacity', 'adjustment' and "
                                 "'percentage' can be specified."))

    action_args['adjustment_type'] = None
    action_args['number'] = None

    if capacity is not None:
        if capacity < 0:
            raise exc.CommandError(_('Cluster capacity must be larger than '
                                     'or equal to zero.'))
        action_args['adjustment_type'] = 'EXACT_CAPACITY'
        action_args['number'] = capacity

    if adjustment is not None:
        if adjustment == 0:
            raise exc.CommandError(_('Adjustment cannot be zero.'))
        action_args['adjustment_type'] = 'CHANGE_IN_CAPACITY'
        action_args['number'] = adjustment

    if percentage is not None:
        if (percentage == 0 or percentage == 0.0):
            raise exc.CommandError(_('Percentage cannot be zero.'))
        action_args['adjustment_type'] = 'CHANGE_IN_PERCENTAGE'
        action_args['number'] = percentage

    if min_step is not None:
        if percentage is None:
            raise exc.CommandError(_('Min step is only used with percentage.'))

    if min_size is not None:
        if min_size < 0:
            raise exc.CommandError(_('Min size cannot be less than zero.'))
        if max_size is not None and max_size >= 0 and min_size > max_size:
            raise exc.CommandError(_('Min size cannot be larger than '
                                     'max size.'))
        if capacity is not None and min_size > capacity:
            raise exc.CommandError(_('Min size cannot be larger than the '
                                     'specified capacity'))

    if max_size is not None:
        if capacity is not None and max_size > 0 and max_size < capacity:
            raise exc.CommandError(_('Max size cannot be less than the '
                                     'specified capacity.'))
        # do a normalization
        if max_size < 0:
            max_size = -1

    action_args['min_size'] = min_size
    action_args['max_size'] = max_size
    action_args['min_step'] = min_step
    action_args['strict'] = args.strict

    resp = service.cluster_resize(args.id, **action_args)
    print('Request accepted by action: %s' % resp['action'])


@utils.arg('-c', '--count', metavar='<COUNT>',
           help=_('Number of nodes to be added to the specified cluster.'))
@utils.arg('id', metavar='<CLUSTER>',
           help=_('Name or ID of cluster to operate on.'))
def do_cluster_scale_out(service, args):
    """Scale out a cluster by the specified number of nodes."""
    show_deprecated('senlin cluster-scale-out', 'openstack cluster expand')
    resp = service.cluster_scale_out(args.id, args.count)
    print('Request accepted by action %s' % resp['action'])


@utils.arg('-c', '--count', metavar='<COUNT>',
           help=_('Number of nodes to be deleted from the specified cluster.'))
@utils.arg('id', metavar='<CLUSTER>',
           help=_('Name or ID of cluster to operate on.'))
def do_cluster_scale_in(service, args):
    """Scale in a cluster by the specified number of nodes."""
    show_deprecated('senlin cluster-scale-in', 'openstack cluster shrink')
    resp = service.cluster_scale_in(args.id, args.count)
    print('Request accepted by action %s' % resp['action'])


@utils.arg('-f', '--filters', metavar='<"KEY1=VALUE1;KEY2=VALUE2...">',
           help=_('Filter parameters to apply on returned results. '
                  'This can be specified multiple times, or once with '
                  'parameters separated by a semicolon.'),
           action='append')
@utils.arg('-o', '--sort', metavar='<SORT_STRING>',
           help=_('Sorting option which is a string containing a list of keys '
                  'separated by commas. Each key can be optionally appended '
                  'by a sort direction (:asc or :desc)'))
@utils.arg('-F', '--full-id', default=False, action="store_true",
           help=_('Print full IDs in list.'))
@utils.arg('id', metavar='<CLUSTER>',
           help=_('Name or ID of cluster to query on.'))
def do_cluster_policy_list(service, args):
    """List policies from cluster."""
    show_deprecated('senlin cluster-policy-list',
                    'openstack cluster policy binding list')
    fields = ['policy_id', 'policy_name', 'policy_type', 'is_enabled']

    cluster = service.get_cluster(args.id)
    queries = {
        'sort': args.sort,
    }

    if args.filters:
        queries.update(utils.format_parameters(args.filters))

    sortby_index = None if args.sort else 3
    policies = service.cluster_policies(cluster.id, **queries)
    formatters = {}
    if not args.full_id:
        formatters = {
            'policy_id': lambda x: x.policy_id[:8]
        }

    utils.print_list(policies, fields, formatters=formatters,
                     sortby_index=sortby_index)


@utils.arg('-p', '--policy', metavar='<POLICY>', required=True,
           help=_('ID or name of the policy to query on.'))
@utils.arg('id', metavar='<CLUSTER>',
           help=_('ID or name of the cluster to query on.'))
def do_cluster_policy_show(service, args):
    """Show a specific policy that is bound to the specified cluster."""
    show_deprecated('senlin cluster-policy-show',
                    'openstack cluster policy binding show')
    binding = service.get_cluster_policy(args.policy, args.id)
    utils.print_dict(binding.to_dict())


@utils.arg('-p', '--policy', metavar='<POLICY>', required=True,
           help=_('ID or name of policy to be attached.'))
@utils.arg('-e', '--enabled', metavar='<BOOLEAN>', default=True,
           help=_('Whether the policy should be enabled once attached. '
                  'Default to enabled.'))
@utils.arg('id', metavar='<NAME or ID>',
           help=_('Name or ID of cluster to operate on.'))
def do_cluster_policy_attach(service, args):
    """Attach policy to cluster."""
    show_deprecated('senlin cluster-policy-attach',
                    'openstack cluster policy attach')
    kwargs = {
        'enabled': strutils.bool_from_string(args.enabled, strict=True),
    }

    resp = service.cluster_attach_policy(args.id, args.policy, **kwargs)
    print('Request accepted by action: %s' % resp['action'])


@utils.arg('-p', '--policy', metavar='<POLICY>', required=True,
           help=_('ID or name of policy to be detached.'))
@utils.arg('id', metavar='<NAME or ID>',
           help=_('Name or ID of cluster to operate on.'))
def do_cluster_policy_detach(service, args):
    """Detach policy from cluster."""
    show_deprecated('senlin cluster-policy-detach',
                    'openstack cluster policy detach')
    resp = service.cluster_detach_policy(args.id, args.policy)
    print('Request accepted by action %s' % resp['action'])


@utils.arg('-p', '--policy', metavar='<POLICY>', required=True,
           help=_('ID or name of policy to be updated.'))
@utils.arg('-e', '--enabled', metavar='<BOOLEAN>',
           help=_('Whether the policy should be enabled.'))
@utils.arg('id', metavar='<NAME or ID>',
           help=_('Name or ID of cluster to operate on.'))
def do_cluster_policy_update(service, args):
    """Update a policy's properties on a cluster."""
    show_deprecated('senlin cluster-policy-update',
                    'openstack cluster policy binding update')
    kwargs = {
        'enabled': strutils.bool_from_string(args.enabled, strict=True),
    }

    resp = service.cluster_update_policy(args.id, args.policy, **kwargs)
    print('Request accepted by action: %s' % resp['action'])


@utils.arg('id', metavar='<CLUSTER>', nargs='+',
           help=_('ID or name of cluster(s) to operate on.'))
def do_cluster_check(service, args):
    """Check the cluster(s)."""
    show_deprecated('senlin cluster-check', 'openstack cluster check')
    for cid in args.id:
        resp = service.check_cluster(cid)
        print('Cluster check request on cluster %(cid)s is accepted by '
              'action %(action)s.' % {'cid': cid, 'action': resp['action']})


@utils.arg('-c', '--check', metavar='<BOOLEAN>', default=False,
           help=_("Whether the cluster should check it's nodes status before "
                  "doing cluster recover. Default is false"))
@utils.arg('id', metavar='<CLUSTER>', nargs='+',
           help=_('ID or name of cluster(s) to operate on.'))
def do_cluster_recover(service, args):
    """Recover the cluster(s)."""
    show_deprecated('senlin cluster-recover', 'openstack cluster recover')

    params = {
        'check': strutils.bool_from_string(args.check, strict=True)
    }

    for cid in args.id:
        resp = service.recover_cluster(cid, **params)
        print('Cluster recover request on cluster %(cid)s is accepted by '
              'action %(action)s.' % {'cid': cid, 'action': resp['action']})


@utils.arg('-p', '--params', metavar='<"KEY1=VALUE1;KEY2=VALUE2...">',
           help=_("Parameter name and values for the operation specified. "
                  "This can be specified multiple times, or once with "
                  "key-value pairs separated by a semicolon."),
           action='append')
@utils.arg('-o', '--operation', metavar='<OPERATION>',
           help=_("Name of an operation to be executed on the cluster."))
@utils.arg('id', metavar='<CLUSTER>',
           help=_('ID or name of a cluster.'))
def do_cluster_op(service, args):
    """Run an operation on a cluster."""
    show_deprecated('senlin cluster-op', 'openstack cluster op')
    params = utils.format_parameters(args.params)

    try:
        service.perform_operation_on_cluster(args.id, args.operation,
                                             **params)
    except exc.HTTPNotFound:
        raise exc.CommandError(_('Cluster "%s" is not found') % args.id)
    print('Request accepted')


# NODES


@utils.arg('-c', '--cluster', metavar='<CLUSTER>',
           help=_('ID or name of cluster from which nodes are to be listed.'))
@utils.arg('-f', '--filters', metavar='<"KEY1=VALUE1;KEY2=VALUE2...">',
           help=_('Filter parameters to apply on returned nodes. '
                  'This can be specified multiple times, or once with '
                  'parameters separated by a semicolon.'),
           action='append')
@utils.arg('-o', '--sort', metavar='<KEY:DIR>',
           help=_('Sorting option which is a string containing a list of keys '
                  'separated by commas. Each key can be optionally appended '
                  'by a sort direction (:asc or :desc)'))
@utils.arg('-l', '--limit', metavar='<LIMIT>',
           help=_('Limit the number of nodes returned.'))
@utils.arg('-m', '--marker', metavar='<ID>',
           help=_('Only return nodes that appear after the given node ID.'))
@utils.arg('-g', '--global-project', default=False, action="store_true",
           help=_('Indicate that this node list should include nodes from '
                  'all projects. This option is subject to access policy '
                  'checking. Default is False.'))
@utils.arg('-F', '--full-id', default=False, action="store_true",
           help=_('Print full IDs in list.'))
def do_node_list(service, args):
    """Show list of nodes."""
    show_deprecated('senlin node-list', 'openstack cluster node list')

    fields = ['id', 'name', 'index', 'status', 'cluster_id', 'physical_id',
              'profile_name', 'created_at', 'updated_at']
    queries = {
        'cluster_id': args.cluster,
        'sort': args.sort,
        'limit': args.limit,
        'marker': args.marker,
        'global_project': args.global_project,
    }

    if args.filters:
        queries.update(utils.format_parameters(args.filters))

    sortby_index = None if args.sort else 6

    nodes = service.nodes(**queries)

    if args.global_project:
        fields.append('project_id')
    if not args.full_id:
        formatters = {
            'id': lambda x: x.id[:8],
            'cluster_id': lambda x: x.cluster_id[:8] if x.cluster_id else '',
            'physical_id': lambda x: x.physical_id[:8] if x.physical_id else ''
        }
        if 'project_id' in fields:
            formatters['project_id'] = lambda x: x.project_id[:8]
    else:
        formatters = {}

    utils.print_list(nodes, fields, formatters=formatters,
                     sortby_index=sortby_index)


def _show_node(service, node_id, show_details=False):
    """Show detailed info about the specified node."""
    try:
        node = service.get_node(node_id, details=show_details)
    except sdk_exc.ResourceNotFound:
        raise exc.CommandError(_('Node not found: %s') % node_id)

    formatters = {
        'metadata': utils.json_formatter,
        'data': utils.json_formatter,
        'dependents': utils.json_formatter,
    }
    data = node.to_dict()
    if show_details and data['details']:
        formatters['details'] = utils.nested_dict_formatter(
            list(data['details'].keys()), ['property', 'value'])

    utils.print_dict(data, formatters=formatters)


@utils.arg('-p', '--profile', metavar='<PROFILE>', required=True,
           help=_('Profile Id or name used for this node.'))
@utils.arg('-c', '--cluster', metavar='<CLUSTER>',
           help=_('Cluster Id for this node.'))
@utils.arg('-r', '--role', metavar='<ROLE>',
           help=_('Role for this node in the specific cluster.'))
@utils.arg('-M', '--metadata', metavar='<"KEY1=VALUE1;KEY2=VALUE2...">',
           help=_('Metadata values to be attached to the node. '
                  'This can be specified multiple times, or once with '
                  'key-value pairs separated by a semicolon.'),
           action='append')
@utils.arg('name', metavar='<NODE_NAME>',
           help=_('Name of the node to create.'))
def do_node_create(service, args):
    """Create the node."""
    show_deprecated('senlin node-create', 'openstack cluster node create')
    attrs = {
        'name': args.name,
        'cluster_id': args.cluster,
        'profile_id': args.profile,
        'role': args.role,
        'metadata': utils.format_parameters(args.metadata),
    }

    node = service.create_node(**attrs)
    _show_node(service, node.id)


@utils.arg('-D', '--details', default=False, action="store_true",
           help=_('Include physical object details.'))
@utils.arg('id', metavar='<NODE>',
           help=_('Name or ID of the node to show the details for.'))
def do_node_show(service, args):
    """Show detailed info about the specified node."""
    show_deprecated('senlin node-show', 'openstack cluster node show')
    _show_node(service, args.id, args.details)


@utils.arg('id', metavar='<NODE>', nargs='+',
           help=_('Name or ID of node(s) to delete.'))
def do_node_delete(service, args):
    """Delete the node(s)."""
    show_deprecated('senlin node-delete', 'openstack cluster node delete')

    result = {}
    for nid in args.id:
        try:
            node = service.delete_node(nid, False)
            result[nid] = ('OK', node.location.split('/')[-1])
        except Exception as ex:
            result[nid] = ('ERROR', six.text_type(ex))

    for rid, res in result.items():
        utils.print_action_result(rid, res)


@utils.arg('-n', '--name', metavar='<NAME>',
           help=_('New name for the node.'))
@utils.arg('-p', '--profile', metavar='<PROFILE ID>',
           help=_('ID or name of new profile to use.'))
@utils.arg('-r', '--role', metavar='<ROLE>',
           help=_('Role for this node in the specific cluster.'))
@utils.arg('-M', '--metadata', metavar='<"KEY1=VALUE1;KEY2=VALUE2...">',
           help=_("Metadata values to be attached to the node. "
                  "This can be specified multiple times, or once with "
                  "key-value pairs separated by a semicolon. Use '{}' "
                  "can clean metadata "),
           action='append')
@utils.arg('id', metavar='<NODE>',
           help=_('Name or ID of node to update.'))
def do_node_update(service, args):
    """Update the node."""
    show_deprecated('senlin node-update', 'openstack cluster node update')
    # Find the node first, we need its UUID
    try:
        node = service.get_node(args.id)
    except sdk_exc.ResourceNotFound:
        raise exc.CommandError(_('Node not found: %s') % args.id)

    attrs = {
        'name': args.name,
        'role': args.role,
        'profile_id': args.profile,
        'metadata': utils.format_parameters(args.metadata),
    }

    service.update_node(node, **attrs)
    _show_node(service, node.id)


@utils.arg('id', metavar='<NODE>', nargs='+',
           help=_('ID or name of node(s) to check.'))
def do_node_check(service, args):
    """Check the node(s)."""
    show_deprecated('senlin node-check', 'openstack cluster node check')
    failure_count = 0

    for nid in args.id:
        try:
            service.check_node(nid)
        except exc.HTTPNotFound:
            failure_count += 1
            print('Node id "%s" not found' % nid)
    if failure_count > 0:
        msg = _('Failed to check some of the specified nodes.')
        raise exc.CommandError(msg)
    print('Request accepted')


@utils.arg('-c', '--check', metavar='<BOOLEAN>', default=False,
           help=_("Whether the node(s) should check physical resource status "
                  "before doing node recover.Default is false"))
@utils.arg('id', metavar='<NODE>', nargs='+',
           help=_('ID or name of node(s) to recover.'))
def do_node_recover(service, args):
    """Recover the node(s)."""
    show_deprecated('senlin node-recover', 'openstack cluster node recover')
    failure_count = 0

    params = {
        'check': strutils.bool_from_string(args.check, strict=True)
    }

    for nid in args.id:
        try:
            service.recover_node(nid, **params)
        except exc.HTTPNotFound:
            failure_count += 1
            print('Node id "%s" not found' % nid)
    if failure_count > 0:
        msg = _('Failed to recover some of the specified nodes.')
        raise exc.CommandError(msg)
    print('Request accepted')


@utils.arg('-p', '--params', metavar='<"KEY1=VALUE1;KEY2=VALUE2...">',
           help=_("Parameter name and values for the operation specified. "
                  "This can be specified multiple times, or once with "
                  "key-value pairs separated by a semicolon."),
           action='append')
@utils.arg('-o', '--operation', metavar='<OPERATION>',
           help=_("Name of an operation to be executed on the node"))
@utils.arg('id', metavar='<NODE>',
           help=_('ID or name of a node.'))
def do_node_op(service, args):
    """Run an operation on a node."""
    show_deprecated('senlin node-op', 'openstack cluster node op')
    if args.params:
        params = utils.format_parameters(args.params)
    else:
        params = {}

    try:
        service.perform_operation_on_node(args.id, args.operation,
                                          **params)
    except exc.HTTPNotFound:
        raise exc.CommandError(_('Node "%s" is not found') % args.id)
    print('Request accepted')


# RECEIVERS


@utils.arg('-f', '--filters', metavar='<"KEY1=VALUE1;KEY2=VALUE2...">',
           help=_('Filter parameters to apply on returned receivers. '
                  'This can be specified multiple times, or once with '
                  'parameters separated by a semicolon.'),
           action='append')
@utils.arg('-l', '--limit', metavar='<LIMIT>',
           help=_('Limit the number of receivers returned.'))
@utils.arg('-m', '--marker', metavar='<ID>',
           help=_('Only return receivers that appear after the given ID.'))
@utils.arg('-o', '--sort', metavar='<KEY:DIR>',
           help=_('Sorting option which is a string containing a list of keys '
                  'separated by commas. Each key can be optionally appended '
                  'by a sort direction (:asc or :desc)'))
@utils.arg('-g', '--global-project', default=False, action="store_true",
           help=_('Indicate that the list should include receivers from'
                  ' all projects. This option is subject to access policy '
                  'checking. Default is False.'))
@utils.arg('-F', '--full-id', default=False, action="store_true",
           help=_('Print full IDs in list.'))
def do_receiver_list(service, args):
    """List receivers that meet the criteria."""
    show_deprecated('senlin receiver-list', 'openstack cluster receiver list')
    fields = ['id', 'name', 'type', 'cluster_id', 'action', 'created_at']
    queries = {
        'limit': args.limit,
        'marker': args.marker,
        'sort': args.sort,
        'global_project': args.global_project,
    }

    if args.filters:
        queries.update(utils.format_parameters(args.filters))

    sortby_index = None if args.sort else 0

    receivers = service.receivers(**queries)
    formatters = {}
    if args.global_project:
        fields.append('project_id')
        fields.append('user_id')
    if not args.full_id:
        formatters = {
            'id': lambda x: x.id[:8],
            'cluster_id': lambda x: x.cluster_id[:8] if x.cluster_id else '-',
        }
        if 'project_id' in fields:
            formatters['project_id'] = lambda x: x.project_id[:8]
            formatters['user_id'] = lambda x: x.user_id[:8]

    utils.print_list(receivers, fields, formatters=formatters,
                     sortby_index=sortby_index)


def _show_receiver(service, receiver_id):
    try:
        receiver = service.get_receiver(receiver_id)
    except sdk_exc.ResourceNotFound:
        raise exc.CommandError(_('Receiver not found: %s') % receiver_id)

    formatters = {
        'actor': utils.json_formatter,
        'params': utils.json_formatter,
        'channel': utils.json_formatter,
    }

    utils.print_dict(receiver.to_dict(), formatters=formatters)


@utils.arg('id', metavar='<RECEIVER>',
           help=_('Name or ID of the receiver to show.'))
def do_receiver_show(service, args):
    """Show the receiver details."""
    show_deprecated('senlin receiver-show', 'openstack cluster receiver show')
    _show_receiver(service, receiver_id=args.id)


@utils.arg('-t', '--type', metavar='<TYPE>', default='webhook',
           help=_('Type of the receiver to create. Receiver type can be '
                  '"webhook" or "message". Default to "webhook".'))
@utils.arg('-c', '--cluster', metavar='<CLUSTER>',
           help=_('Targeted cluster for this receiver. Required if receiver '
                  'type is webhook.'))
@utils.arg('-a', '--action', metavar='<ACTION>',
           help=_('Name or ID of the targeted action to be triggered. '
                  'Required if receiver type is webhook.'))
@utils.arg('-P', '--params', metavar='<"KEY1=VALUE1;KEY2=VALUE2...">',
           help=_('A dictionary of parameters that will be passed to target '
                  'action when the receiver is triggered.'),
           action='append')
@utils.arg('name', metavar='<NAME>',
           help=_('Name of the receiver to create.'))
def do_receiver_create(service, args):
    """Create a receiver."""
    show_deprecated('senlin receiver-create',
                    'openstack cluster receiver create')

    if args.type == 'webhook':
        if (not args.cluster or not args.action):
            msg = _('cluster and action parameters are required to create '
                    'webhook type of receiver.')
            raise exc.CommandError(msg)

    params = {
        'name': args.name,
        'type': args.type,
        'cluster_id': args.cluster,
        'action': args.action,
        'params': utils.format_parameters(args.params)
    }

    receiver = service.create_receiver(**params)
    _show_receiver(service, receiver.id)


@utils.arg('-n', '--name', metavar='<NAME>',
           help=_('The new name for the receiver.'))
@utils.arg('-a', '--action', metavar='<ACTION>',
           help=_('Name or ID of the targeted action to be triggered. '
                  'Required if receiver type is webhook.'))
@utils.arg('-P', '--params', metavar='<"KEY1=VALUE1;KEY2=VALUE2...">',
           help=_('A dictionary of parameters that will be passed to target '
                  'action when the receiver is triggered.'),
           action='append')
@utils.arg('id', metavar='<receiver>',
           help=_('Name or ID of receiver to update.'))
def do_receiver_update(service, args):
    """Update a receiver."""
    show_deprecated('senlin receiver-update',
                    'openstack cluster receiver update')
    params = {
        'name': args.name,
        'action': args.action,
        'params': utils.format_parameters(args.params)
    }

    # Find the receiver first, we need its id
    try:
        receiver = service.get_receiver(args.id)
    except sdk_exc.ResourceNotFound:
        raise exc.CommandError(_('Receiver not found: %s') % args.id)
    service.update_receiver(receiver, **params)
    _show_receiver(service, receiver.id)


@utils.arg('id', metavar='<RECEIVER>', nargs='+',
           help=_('Name or ID of receiver(s) to delete.'))
def do_receiver_delete(service, args):
    """Delete receiver(s)."""
    show_deprecated('senlin receiver-delete',
                    'openstack cluster receiver delete')
    failure_count = 0

    for wid in args.id:
        try:
            service.delete_receiver(wid, False)
        except Exception as ex:
            failure_count += 1
            print(ex)
    if failure_count > 0:
        msg = _('Failed to delete some of the specified receiver(s).')
        raise exc.CommandError(msg)
    print('Receivers deleted: %s' % args.id)


# EVENTS


@utils.arg('-f', '--filters', metavar='<"KEY1=VALUE1;KEY2=VALUE2...">',
           help=_('Filter parameters to apply on returned events. '
                  'This can be specified multiple times, or once with '
                  'parameters separated by a semicolon.'),
           action='append')
@utils.arg('-l', '--limit', metavar='<LIMIT>',
           help=_('Limit the number of events returned.'))
@utils.arg('-m', '--marker', metavar='<ID>',
           help=_('Only return events that appear after the given event ID.'))
@utils.arg('-o', '--sort', metavar='<KEY:DIR>',
           help=_('Sorting option which is a string containing a list of keys '
                  'separated by commas. Each key can be optionally appended '
                  'by a sort direction (:asc or :desc)'))
@utils.arg('-g', '--global-project', default=False, action="store_true",
           help=_('Whether events from all projects should be listed. '
                  ' Default to False. Setting this to True may demand '
                  'for an admin privilege.'))
@utils.arg('-F', '--full-id', default=False, action="store_true",
           help=_('Print full IDs in list.'))
def do_event_list(service, args):
    """List events."""
    show_deprecated('senlin event-list', 'openstack cluster event list')
    fields = ['id', 'generated_at', 'obj_type', 'obj_id', 'obj_name', 'action',
              'status', 'level', 'cluster_id']
    field_labels = ['id', 'timestamp', 'obj_type', 'obj_id', 'obj_name',
                    'action', 'status', 'level', 'cluster_id']

    queries = {
        'sort': args.sort,
        'limit': args.limit,
        'marker': args.marker,
        'global_project': args.global_project,
    }

    if args.filters:
        queries.update(utils.format_parameters(args.filters))

    sortby_index = None if args.sort else 0

    formatters = {}
    if args.global_project:
        fields.append('project_id')
        field_labels.append('project_id')
    if not args.full_id:
        formatters['id'] = lambda x: x.id[:8]
        formatters['obj_id'] = lambda x: x.obj_id[:8] if x.obj_id else ''
        formatters['cluster_id'] = (lambda x: x.cluster_id[:8]
                                    if x.cluster_id else '')
        if 'project_id' in fields:
            formatters['project_id'] = lambda x: x.project_id[:8]

    events = service.events(**queries)
    utils.print_list(events, fields, formatters=formatters,
                     sortby_index=sortby_index, field_labels=field_labels)


@utils.arg('id', metavar='<EVENT>',
           help=_('ID of event to display details for.'))
def do_event_show(service, args):
    """Describe the event."""
    show_deprecated('senlin event-show', 'openstack cluster event show')
    try:
        event = service.get_event(args.id)
    except sdk_exc.ResourceNotFound:
        raise exc.CommandError(_("Event not found: %s") % args.id)

    utils.print_dict(event.to_dict())


# ACTIONS


@utils.arg('-f', '--filters', metavar='<"KEY1=VALUE1;KEY2=VALUE2...">',
           help=_('Filter parameters to apply on returned actions. '
                  'This can be specified multiple times, or once with '
                  'parameters separated by a semicolon.'),
           action='append')
@utils.arg('-o', '--sort', metavar='<KEY:DIR>',
           help=_('Sorting option which is a string containing a list of keys '
                  'separated by commas. Each key can be optionally appended '
                  'by a sort direction (:asc or :desc)'))
@utils.arg('-l', '--limit', metavar='<LIMIT>',
           help=_('Limit the number of actions returned.'))
@utils.arg('-m', '--marker', metavar='<ID>',
           help=_('Only return actions that appear after the given node ID.'))
@utils.arg('-g', '--global-project', default=False, action="store_true",
           help=_('Whether actions from all projects should be listed. '
                  ' Default to False. Setting this to True may demand '
                  'for an admin privilege.'))
@utils.arg('-F', '--full-id', default=False, action="store_true",
           help=_('Print full IDs in list.'))
def do_action_list(service, args):
    """List actions."""
    show_deprecated('senlin action-list', 'openstack cluster action list')
    fields = ['id', 'name', 'action', 'status', 'target_id', 'depends_on',
              'depended_by', 'created_at']

    queries = {
        'sort': args.sort,
        'limit': args.limit,
        'marker': args.marker,
        'global_project': args.global_project,
    }

    if args.filters:
        queries.update(utils.format_parameters(args.filters))

    sortby_index = None if args.sort else 0

    actions = service.actions(**queries)

    formatters = {}
    s = None
    if not args.full_id:
        s = 8
        formatters['id'] = lambda x: x.id[:s]
        formatters['target_id'] = lambda x: x.target_id[:s]

    formatters['depends_on'] = lambda x: '\n'.join(a[:s] for a in x.depends_on)
    formatters['depended_by'] = lambda x: '\n'.join(a[:s] for a in x.
                                                    depended_by)

    utils.print_list(actions, fields, formatters=formatters,
                     sortby_index=sortby_index)


@utils.arg('id', metavar='<ACTION>',
           help=_('Name or ID of the action to show the details for.'))
def do_action_show(service, args):
    """Show detailed info about the specified action."""
    show_deprecated('senlin action-show', 'openstack cluster action show')
    try:
        action = service.get_action(args.id)
    except sdk_exc.ResourceNotFound:
        raise exc.CommandError(_('Action not found: %s') % args.id)

    formatters = {
        'inputs': utils.json_formatter,
        'outputs': utils.json_formatter,
        'metadata': utils.json_formatter,
        'data': utils.json_formatter,
        'depends_on': utils.list_formatter,
        'depended_by': utils.list_formatter,
    }

    utils.print_dict(action.to_dict(), formatters=formatters)


def do_service_list(service, args=None):
    """Show a list of all running services."""
    show_deprecated('senlin service-list',
                    'openstack cluster service list')
    fields = ['binary', 'host', 'status', 'state', 'updated_at',
              'disabled_reason']
    queries = {}
    result = service.services(**queries)

    formatters = {}
    utils.print_list(result, fields, formatters=formatters)
