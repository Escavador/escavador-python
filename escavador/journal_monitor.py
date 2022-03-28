from escavador.method import Method
from escavador.exceptions import InvalidParamsException


class JournalMonitor(object):

    def __init__(self):
        self.methods = Method()

    def get_monitor_journal(self, monitor_id):
        """
        Return the journals from a monitor
        :param monitor_id: the monitor ID
        :return: json containing all ter journals associated with the monitor
        """

        return self.methods.get("/monitoramentos/{}/origens".format(monitor_id))

    def create_monitor(self, monitor_type, **kwargs):
        """
        Create a new monitor to words or lawsuit
        :param monitor_type: the type of monitor (termo or processo)
        :keyword arguments:
            **termo**(``string``) -- the word to be monitored, required if monitor_type == termo
            **origens_ids**(``int[]``) -- array with jounals ids to be monitored
            **processo_id**(``string``) -- the lawsuit id to be monitored
            **variacoes**(``string[]``) -- array with variations of the monitored word
            **termos_auxiliares**(``string[][]``) -- multidimensional array with words and conditions to the monitorm alert
        :return: json with the new monitor
        """

        if monitor_type not in ['termo','processo']:
            raise InvalidParamsException("the monitor type must be one of the following: termo or processo")

        data = {
            'tipo': monitor_type,
            'termo': kwargs.get('termo'),
            'origens_id': kwargs.get('origens_id'),
            'processo_id': kwargs.get('processo_id'),
            'variacoes': kwargs.get('variacoes'),
            'termos_auxiliares': kwargs('termos_auxiliares')
        }

        return self.methods.post("/monitoramentos", data=data)

    def get_monitors(self):
        """
        Return all monitors of the user
        :return: json containing all monitors of the user
        """

        return self.methods.get("/monitoramentos")

    def get_monitor(self, monitor_id):
        """
        Return a monitor based on the id
        :param monitor_id the monitor ID
        :return: json containing all monitors of the user
        """

        return self.methods.get("/monitoramentos/{}".format(monitor_id))

    def update_monitor(self, monitor_id, **kwargs):
        """
        Update the journals and the word variations of a monitor
        :param monitor_id: the monitor ID
        :keyword arguments:
            **variacoes**(``string[]``) -- array with variations of the monitored word
            **origens_ids**(``int[]``) -- array with journals ids to be monitored
        :return: json containing the updated monitor
        """
        data = {
            'variacoes': kwargs.get('variacoes'),
            'origens_ids': kwargs.get('origens_ids')
        }

        return self.methods.put("monitoramentos/{}".format(monitor_id), data=data)

    def remove_monitor(self,monitor_id):
        """
        Remove a monitor based on the monitor ID
        :param monitor_id: the monitor ID
        :return: sucess|NotFound
        """

        return self.methods.delete("/monitoramentos/{}".format(monitor_id))
