from rest_framework import serializers

class PollutantSerializer(serializers.HyperlinkModelSerializer):
    class Meta:
        model=server
        #fields=('url')
