import collections


class XmlListTupleConfig(list):
    def __init__(self, parent_element, **kwargs):
        super(XmlListTupleConfig, self).__init__(**kwargs)
        for element in parent_element:
            if element:
                list_of_tuple = XmlListTupleConfig(element)
                if element.items():
                    list_of_tuple.append(element.items())
                self.extend([(element.tag, XmlListTupleConfig)])
            elif element.items():
                self.extend([(element.tag, element.items())])
            else:
                self.extend([(element.tag, element.text)])


class XmlListConfig(list):
    def __init__(self, a_list):
        super(XmlListConfig, self).__init__()
        for element in a_list:
            if element:
                self.append(XmlListTupleConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)


class XmlDictConfig(collections.OrderedDict):
    """
    Example usage:

    tree = ElementTree.parse('your_file.xml')
    root = tree.getroot()
    xml_list_of_dicts = XmlDictConfig(root)

    Or, if you want to use an XML string:

    root = ElementTree.XML(xml_string)
    xml_list_of_dicts = XmlDictConfig(root)

    And then use xml_list_of_dicts for what it is... a dict.
    """

    def __init__(self, parent_element, **kwargs):
        super(XmlDictConfig, self).__init__(**kwargs)
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                if is_convertible_to_list_of_tuples(element):
                    aDict = XmlDictConfig(element)
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself
                    aDict = {element[0].tag: XmlListConfig(element)}
                # if the tag has attributes, add those to the dict
                if element.items():
                    aDict.update(dict(element.items()))
                self.update({element.tag: aDict})
            # this assumes that if you've got an attribute in a tag,
            # you won't be having any text. This may or may not be a
            # good idea -- time will tell. It works for the way we are
            # currently doing XML configuration files...
            elif element.items():
                self.update({element.tag: dict(element.items())})
            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                self.update([(element.tag, element.text)])


def is_convertible_to_list_of_tuples(some_iterable):
    return len(some_iterable) == 1 or any([some_element.tag != some_iterable[0].tag for some_element in some_iterable])
