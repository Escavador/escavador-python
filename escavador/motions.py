from escavador.method import Method


class Motions(object):

    def __init__(self):
        self.methods = Method()

    def get_motion(self, motion_id):
        """
        Return a motion based on the motion ID \n
        :param motion_id: the motion ID \n
        :return: a json containing the motion
        """
        return self.methods.get("/movimentacoes/{}".format(motion_id))