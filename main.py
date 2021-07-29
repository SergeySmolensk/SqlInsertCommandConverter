import re

FULL_TAG_PATTERN_EXPRESSION = "['a-z]+:[^,)]*"
ROLES_PATTERN_EXPRESSION = "'\[[\"\w\",\s]*]'"
PREFIX_TAG_PATTERN_EXPRESSION = "TAG."
USED_DELIMITER = ','
FILE_NAME = "dbcreate.sql"
TABLE_NAME = "all_tags"
DEFAULT_ROLES = "'[\"admin\"]'"
NEED_FIND_ROLES = False


def createInsertScript(tag_info, table_name):
    with open("insertTags.sql", "w") as fw:
        i = 0
        elements_count = len(tag_info)
        while i < elements_count:
            print("INSERT INTO " + table_name + " VALUES(" + str(tag_info[i]) + "," + str(tag_info[i + 1]) + "," +
                  str(tag_info[i + 2]) + ");")
            fw.write("INSERT INTO " + table_name + " VALUES(" + str(tag_info[i]) + "," + str(tag_info[i + 1]) + "," +
                     str(tag_info[i + 2]) + ");\n")
            i = i + 3


def getTagsInfo(file_name):
    tags_info = []
    searched_roles = None
    with open(file_name, 'r') as fileReader:
        file_info = fileReader.read()
        tags_result = re.findall(FULL_TAG_PATTERN_EXPRESSION, file_info)
        if NEED_FIND_ROLES:
            searched_roles = iter(re.findall(ROLES_PATTERN_EXPRESSION, file_info))
        for tag in tags_result:
            tag_name = "'" + tag[7:]
            tags_info.append(tag_name)
            tags_info.append(getDataTypeCode(tag[1]))
            tags_info.append(DEFAULT_ROLES)
        if NEED_FIND_ROLES:
            for i in range(1, len(tags_info), 2):
                tags_info[i] = next(searched_roles)
    return tags_info


def getDataTypeCode(data_type_character):
    if data_type_character == "s":
        return 54
    elif data_type_character == "d":
        return 18
    elif data_type_character == "i":
        return 15
    else:
        return None


if __name__ == '__main__':
    tagInfo = getTagsInfo(FILE_NAME)
    createInsertScript(tagInfo, TABLE_NAME)
