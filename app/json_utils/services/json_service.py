from abc import abstractmethod, ABC
from datetime import date, datetime, time
from decimal import Decimal
from uuid import UUID


class TypeConverter(ABC):
    @abstractmethod
    def canHandle(self, obj) -> bool:
        pass

    @abstractmethod
    def convert(self, obj):
        pass


class JsonTypeConverter(TypeConverter):
    def canHandle(self, obj) -> bool:
        return isinstance(obj, (int, float, str, bool))
    def convert(self, obj):
        return obj


class DateTypeConverter(TypeConverter):
    def canHandle(self, obj) -> bool:
        return isinstance(obj, (date, datetime))
    def convert(self, obj):
        return obj.isoformat()


class TimeTypeConverter(TypeConverter):
    def canHandle(self, obj) -> bool:
        return isinstance(obj, time)
    def convert(self, obj):
        return obj.isoformat()


class DecimalTypeConverter(TypeConverter):
    def canHandle(self, obj) -> bool:
        return isinstance(obj, Decimal)
    def convert(self, obj):
        return float(obj)


class UUIDTypeConverter(TypeConverter):
    def canHandle(self, obj) -> bool:
        return isinstance(obj, UUID)
    def convert(self, obj):
        return str(obj)


class ByteTypeConverter(TypeConverter):
    def canHandle(self, obj) -> bool:
        return isinstance(obj, bytes)
    def convert(self, obj):
        try:
            return obj.decode("utf-8")
        except Exception:
            import base64
            return base64.b64encode(obj).decode("utf-8")

TYPE_CONVERTERS: list[TypeConverter] = [
        JsonTypeConverter(),
        DateTypeConverter(),
        TimeTypeConverter(),
        DecimalTypeConverter(),
        UUIDTypeConverter(),
        ByteTypeConverter()
]

def make_json_safe(obj):
    if obj is None:
        return None

    for converter in TYPE_CONVERTERS:
        if converter.canHandle(obj):
            return converter.convert(obj)

    if isinstance(obj, (list, tuple)):
        return [make_json_safe(v) for v in obj]

    if isinstance(obj, dict):
        return {k: make_json_safe(v) for k, v in obj.items()}

    return str(obj)