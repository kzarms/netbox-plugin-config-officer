"""Class for config text functions."""

import re

import diffios


def get_lines_in_section(config, section):
    """Get lines (i.e ip address x.x.x.x) under the section's name.

    i.e. interface GigabitEthernet0

    # noqa: DAR201
    # noqa: DAR101

    """
    output = []
    if section in config:
        if config.index(section) == len(config):
            return []

        for i in range(config.index(section) + 1, len(config)):  # noqa: WPS111,WPS518,E501
            line = config[i]
            if re.search(r'^ ', line):
                output.append(line)
                if section in config:
                    config[config.index(section)] = '##_##'
                config[i] = '##_##'
            else:
                break
        return output
    return []


def is_section(config, line):
    """Def ines if this line - is section's name interface GigabitEthernet 0.

    # noqa: DAR201
    # noqa: DAR101

    """
    if config.index(line) + 1 == len(config):
        return False
    if re.match(r'^ ', line):
        return False
    if re.match(r'^ ', config[config.index(line) + 1]):
        return True
    # Nothing else, return False
    return False


def merge_configs(config1, config2):
    """Merge to config with the same sections.

    # noqa: DAR201
    # noqa: DAR101

    """
    output = []

    if config1:
        for line in config1:
            output.append(line)
            if line in config2:
                if is_section(config1, line):
                    for conf2_line in get_lines_in_section(config2, line):
                        output.append(conf2_line)  # noqa: WPS220
        output.append('!')
    if config2:
        for line2 in config2:
            if line2 != '##_##':
                output.append(line2)
        output.append('!')
    return output


def get_config_diff(template, config, ignore=None):
    """Get inconsistency between device running config and template.

    # noqa: DAR201
    # noqa: DAR101

    """
    if not ignore:
        ignore = [
            'Building configuration',
            'Current configuration',
            'NVRAM config last updated',
            'Last configuration change',
        ]

    diff = diffios.Compare(template, config, ignore)

    # Get lines that exist in template only
    return diff.missing()


def generate_templates_config_for_device(templates):
    """
    Merge config from matched templates and changes due to vars.

    # noqa: DAR201
    # noqa: DAR101

    """
    config = []
    for template in templates:
        config = merge_configs(config, template.configuration.splitlines())
    return '\n'.join(config)
