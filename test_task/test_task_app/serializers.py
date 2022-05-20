from cProfile import label
from rest_framework import serializers

class CreateRequestSerrializer(serializers.Serializer):

    """
    Серіалайзер для запиту зі створення запиту
    """

    id_from = serializers.IntegerField()
    id_to = serializers.IntegerField()

    def validate(self, data):
        """
        Перевіряємо чи правильно перший індекс більше/дорівнює останньому
        """
        
        if data['id_from'] >= data['id_to']:
            raise serializers.ValidationError('"to" parameter must be bigger or equal then "to" from')

        return data
        

    def __init__(self, *args, **kwargs):
        super(CreateRequestSerrializer, self).__init__(*args, **kwargs)
        #Перейменовуємо поля для відповідності ТЗ
        self.fields['from'] = self.fields['id_from']
        self.fields['to'] = self.fields['id_to']

        del self.fields['id_from']
        del self.fields['id_to']


class GetRequestInfoSerrializer(serializers.Serializer):
    
    """
    Серіалайзер для отримання інформації по понкретному запиту
    """
    request_id = serializers.CharField()


class GetGoodsInfoSerrializer(serializers.Serializer):
    
    """
    Серіалайзер для отримання переліку товарів по фільтру за об'ємом і вагою
    """
    
    volume_min = serializers.FloatField(required=False)
    volume_max = serializers.FloatField(required=False)
    weight_min = serializers.FloatField(required=False)
    weight_max = serializers.FloatField(required=False)




