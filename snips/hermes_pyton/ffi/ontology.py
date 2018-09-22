from __future__ import absolute_import
from __future__ import unicode_literals

from ctypes import c_char_p, c_int32, c_int64, c_int, c_float, c_uint8, c_void_p, POINTER, pointer, Structure, byref


class CStringArray(Structure):
    _fields_ = [
        ("data", POINTER(c_char_p)),
        ("size", c_int32)
    ]


class CProtocolHandler(Structure):
    _fields_ = [("handler", c_void_p)]


class CTtsFacade(Structure):
    _fields_ = [("facade", c_void_p)]


class CDialogueFacade(Structure):
    _fields_ = [("facade", c_void_p)]


class CSayMessage(Structure):
    _fields_ = [("text", c_char_p),
                ("lang", c_char_p),
                ("id", c_char_p),
                ("site_id", c_char_p),
                ("session_id", c_char_p)]


class CSayFinishedMessage(Structure):
    _fields_ = [("id", POINTER(c_char_p)),
                ("session_id", POINTER(c_char_p))]


class CContinueSessionMessage(Structure):
    _fields_ = [("session_id", c_char_p),
                ("text", c_char_p),
                ("intent_filter", POINTER(CStringArray))]

    @classmethod
    def build(cls, session_id, text, intent_filter):
        session_id = session_id.encode('utf-8')
        text = text.encode('utf-8')
        intent_filter = [intent_filter_item.encode('utf-8') for intent_filter_item in intent_filter]

        c_intent_filter = CStringArray()
        c_intent_filter.size = c_int(len(intent_filter))
        c_intent_filter.data = (c_char_p * len(intent_filter))(*intent_filter)

        cContinueSessionMessage = cls(session_id, text, pointer(c_intent_filter))
        return cContinueSessionMessage


class CEndSessionMessage(Structure):
    _fields_ = [("session_id", c_char_p),
                ("text", c_char_p)]

    @classmethod
    def build(cls, session_id, text):
        return cls(session_id.encode('utf-8'), text.encode('utf-8'))

class CSessionInit(Structure):
    _fields_ = [("init_type", c_int32)]  # 1 : Action, 2: Notification

class CActionSessionInit(Structure):
    _fields_ = [("text", c_char_p),
                ("intent_filter", POINTER(CStringArray)),
                ("can_be_enqueued", c_uint8)] \

    @classmethod
    def build(cls, text, intent_filter, can_be_enqueued_boolean):
        text = text.encode('utf-8')
        intent_filter = [intent_filter_item.encode('utf-8') for intent_filter_item in intent_filter]

        c_intent_filter = CStringArray()
        c_intent_filter.size = c_int(len(intent_filter))
        c_intent_filter.data = (c_char_p * len(intent_filter))(*intent_filter)

        can_be_enqueued = 1 if can_be_enqueued_boolean else 0

        return cls(text, pointer(c_intent_filter), can_be_enqueued)


class CSessionInitAction(CSessionInit):
    _fields_ = [("value", POINTER(CActionSessionInit))]

    @classmethod
    def build(cls, text, intent_filter, can_be_enqueued_boolean):
        text = text.encode('utf-8')
        intent_filter = [intent_filter_item.encode('utf-8') for intent_filter_item in intent_filter]

        cActionSessionInit = CActionSessionInit.build(text, intent_filter, can_be_enqueued_boolean)
        return cls(c_int(1), pointer(cActionSessionInit))


class CSessionInitNotification(CSessionInit):
    _fields_ = [("value", c_char_p)]

    @classmethod
    def build(cls, value):
        return cls(c_int(0), value.encode('utf-8'))


class CStartSessionMessageAction(Structure):
    _fields_ = [("init", CSessionInitAction),
                ("custom_data", c_char_p),
                ("site_id", c_char_p)]

    @classmethod
    def build(cls, init, custom_data, site_id):
        custom_data = custom_data.encode('utf-8')
        site_id = site_id.encode('utf-8')
        return cls(init, custom_data, site_id)

class CStartSessionMessageNotification(Structure):
    _fields_ = [("init", CSessionInitNotification),
                ("custom_data", c_char_p),
                ("site_id", c_char_p)]

    @classmethod
    def build(cls, init, custom_data, site_id):
        custom_data = custom_data.encode('utf-8')
        site_id = site_id.encode('utf-8')
        return cls(init, custom_data, site_id)



class CIntentClassifierResult(Structure):
    _fields_ = [("intent_name", c_char_p),
                ("probability", c_float)]


class CSlotValue(Structure):
    _fields_ = [
        ("value", c_void_p),
        ("value_type", c_int32) # TODO : value_type is an enum
    ]


class CSlot(Structure):
    _fields_ = [
        ("value", CSlotValue),
        ("raw_value", c_char_p),
        ("entity", c_char_p),
        ("slot_name", c_char_p),
        ("range_start", c_int32),
        ("range_end", c_int32)
    ]


class CNluSlot(Structure):
    _fields_ = [
        ("confidence", c_float),
        ("nlu_slot", POINTER(CSlot))
    ]


class CSlotList(Structure):
    _fields_ = [
        ("slots", POINTER(CSlot)),
        ("size", c_int32)
    ]

class CNluSlotArray(Structure):
    _fields_ = [
        ("entries", POINTER(POINTER(CNluSlot))), # *const *const CNluSlot,
        ("count", c_int)
    ]

class CIntentMessage(Structure):
    _fields_ = [("session_id", c_char_p),
                ("custom_data", c_char_p),
                ("site_id", c_char_p),
                ("input", c_char_p),
                ("intent", POINTER(CIntentClassifierResult)),
                ("slots", POINTER(CNluSlotArray))]

class CSessionTermination(Structure):
    _fields_ = [("termination_type", c_int),
                ("data", c_char_p)]

class CSessionEndedMessage(Structure):
    _fields_ = [("session_id", c_char_p),
                ("custom_data", c_char_p),
                ("termination", CSessionTermination),
                ("site_id", c_char_p)]


class CSessionQueuedMessage(Structure):
    _fields_ = [("session_id", c_char_p),
                ("custom_data", c_char_p),
                ("site_id", c_char_p)]


class CSessionStartedMessage(Structure):
    _fields_ = [("session_id", c_char_p),
                ("custom_data", c_char_p),
                ("site_id", c_char_p),
                ("reactivated_from_session_id", c_char_p)]



# Slot Types Structs

class CAmountOfMoneyValue(Structure):
    _fields_ = [("unit", c_char_p),
                ("value", c_float),
                ("precision", c_int)] # TODO : Precision is an enum.


class CTemperatureValue(Structure):
    _fields_ = [("unit", c_char_p),
                ("value", c_float)]



class CInstantTimeValue(Structure):
    _fields_ = [("value", c_char_p),
               ("grain", c_int), # TODO : CGrain is an enum ...
               ("precision", c_int)] # TODO : Precision is an enum ...


class CTimeIntervalValue(Structure):
    _fields_ = [("from_date", c_char_p),
                ("to_date", c_char_p)]

class CDurationValue(Structure):
    _fields_ = [("years", c_int64),
                ("quarters", c_int64),
                ("months", c_int64),
                ("weeks", c_int64),
                ("days", c_int64),
                ("hours", c_int64),
                ("minutes", c_int64),
                ("seconds", c_int64),
                ("precision", c_int)]

