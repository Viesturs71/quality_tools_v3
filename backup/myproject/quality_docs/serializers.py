from rest_framework import serializers

from .models.approval_flow import ApprovalFlow
from .models.documents import QualityDocument


class QualityDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = QualityDocument
        fields = "__all__"

class ApprovalFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalFlow
        fields = "__all__"
