class Culture:
    English: str = 'en-us'
    Chinese: str = 'zh-cn'
    Spanish: str = 'es-es'
    Portuguese: str = 'pt-br'
    French: str = 'fr-fr'
    Japanese: str = 'ja-jp'
    Dutch: str = 'nl-nl'
    Korean: str = 'ko-kr'
    Italian: str = 'it-it'

class BaseCultureInfo:
    def __init__(self, culture_code: str):
        self.code: str = culture_code

    def format(self, value: object) -> str:
        return repr(value)
