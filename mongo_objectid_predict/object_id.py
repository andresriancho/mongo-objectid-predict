import time


class ObjectId(object):
    """
    The 12-byte ObjectId value consists of:

        a 4-byte value representing the seconds since the Unix epoch,
        a 3-byte machine identifier,
        a 2-byte process id, and
        a 3-byte counter, starting with a random value.
    """
    def __init__(self, object_id):
        epoch, machine, process, counter = ObjectId.parse(object_id)

        self.epoch = epoch
        self.machine = machine
        self.process = process
        self.counter = counter

    def __str__(self):
        return '%08x%s%s%06x' % (self.epoch,
                                 self.machine,
                                 self.process,
                                 self.counter)

    def __repr__(self):
        args = (self.epoch, self.machine, self.process, self.counter)
        return '<ObjectId: (e: %s, m: %s, p: %s, c: %s)>' % args

    def copy(self):
        return ObjectId(str(self))

    @staticmethod
    def parse(object_id):
        epoch = int(object_id[:8], 16)
        machine = object_id[8:14]
        process = object_id[14:18]
        counter = int(object_id[18:24], 16)

        return epoch, machine, process, counter

    @staticmethod
    def looks_like(object_id):
        """
        :param object_id: A string with a mongo object ID
        :return: (True if it looks like a mongo object ID,
                  reason when False is sent in the first element of the tuple)
        """
        if len(object_id) != 24:
            return False, 'Mongo ObjectIds have 12 bytes'

        for c in object_id:
            if c not in '0123456789abcdef':
                return False, 'Mongo ObjectIds are [a-f0-9]'

        object_id_epoch = int(object_id[:8], 16)
        our_epoch = int(time.time())
        one_day = 24 * 60 * 60

        if object_id_epoch > our_epoch + one_day:
            return False, 'Mongo ObjectId epoch (%s) is too far in the future' % object_id_epoch

        if object_id_epoch < our_epoch - one_day * 365:
            return False, 'Mongo ObjectId epoch (%s) is too far in the past' % object_id_epoch

        return True, None
