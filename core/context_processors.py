from core.models import Company


def company_info(_request):
    return {"company_info": Company.objects.first()}
