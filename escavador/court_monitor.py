from escavador.endpoint import Endpoint
from escavador.exceptions import InvalidParamsException


class CourtMonitor(Endpoint):

    def get_monitors(self):
        """
        Return all the user court monitors
        :return: json containing all the court monitors
        """

        return self.methods.get("/monitoramentos-tribunal")

    def get_monitor(self, monitor_id):
        """
        Return a user court monitor based on the ID
        :param monitor_id: the monitor ID
        :return: json containing all the court monitors
        """

        return self.methods.get("/monitoramentos-tribunal/{}".format(monitor_id))

    def update_monitor(self, monitor_id, **kwargs):
        """
        Updates a monitor frequency based on its ID
        :param monitor_id: the monitor ID
        :keyword arguments:
            **frequencia**(``string``) -- The frequency the monitor will search
        :return: sucess|NotFound
        """
        data = {
            'frequencia': kwargs.get('frequencia')
        }
        return self.methods.put("/monitoramentos-tribunal/{}".format(monitor_id), data=data)

    def create_monitor(self, monitor_type,value, **kwargs):
        """
        Create a court monitor
        :param monitor_type: the type of monitor, available options (UNICO, NUMDOC ,NOME)
        :param value: the value that will be monitored in the court
        :keyword arguments:
            **frequencia**(``string``) -- The frequency the monitor will search
            **courts**(``string``) -- an array of courts to monitor the value
        :return: json containing the monitor information
        """

        available_types = ['UNICO', 'NUMDOC', 'NOME']

        if monitor_type not in available_types:
            raise InvalidParamsException("Invalid monitor type")

        if (monitor_type == 'UNICO') and (kwargs.get('courts') is None):
            raise  InvalidParamsException("The court must be sent if the monitor type is UNICO")

        data = {
            'tipo': monitor_type,
            'value': value,
            'court': kwargs.get('court'),
            'frequencia': kwargs.get('frequencia')
        }

        return self.methods.post("/monitoramento-tribunal", data=data)

    def delete_monitor(self, monitor_id):
        """
        Delete a monitor based on its ID
        :param monitor_id: the monitor ID
        :return: json containing the monitor information | NotFound
        """

        return self.methods.delete("/monitoramentos-tribunal/{}".format(monitor_id));