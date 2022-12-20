class T24ResponseWorker:

    def __init__(self, resp: str):
        if resp:
            if resp[0] == ',':
                resp = resp[1:]
            self.resp_list = resp.split(",\"")
            self.columns = self.resp_list[0].split("/")
            if len(self.columns) > 1:
                for index, column in enumerate(self.columns):
                    newcolumn = column.split("::")[0]
                    self.columns[index] = newcolumn
            self.resp_list = self.resp_list[1:]

    def get_response_list(self):
        list_obj = []
        from robot.api import logger
        if len(self.resp_list) >= 0:
            for values in self.resp_list:
                f_values = values.replace('"', "").split("\t")
                if len(self.columns) <= 1:
                    self.columns.clear()
                    for index, value in enumerate(f_values):
                        self.columns.append(str(index))
                obj = T24Response(self.columns)
                if len(f_values) == len(self.columns):
                    for index, column in enumerate(self.columns):
                        obj.__setattr__(column, f_values.__getitem__(index).strip())
                    list_obj.append(obj.__dict__)
        logger.console("- Response Headers: " + str(self.columns))
        logger.console("- Response Objects: " + str(len(list_obj)))
        return list_obj


class T24Response(object):
    def __init__(self, columns):
        for key in columns:
            self.__dict__[key] = ""

    def __getattr__(self, key):
        return self.__dict__[key]

    def __setattr__(self, key, value):
        self.__dict__[key] = value
