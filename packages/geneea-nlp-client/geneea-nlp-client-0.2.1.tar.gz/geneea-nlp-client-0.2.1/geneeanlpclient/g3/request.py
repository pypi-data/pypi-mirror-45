# Copyright 2019 Geneea Analytics s.r.o.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from enum import Enum
from typing import NamedTuple, List, Optional

from geneeanlpclient.common.dictutil import JsonType


class ParaSpec(NamedTuple):
    type: str
    """ Type of the paragraphs, typically one of Paragraph.TYPE_TITLE, Paragraph.TYPE_LEAD, Paragraph.TYPE_TEXT; 
    possibly Paragraph.TYPE_SECTION_HEADING  """
    text: str
    """ Text of the paragraph """


class AnalysisType(Enum):
    ALL = 1
    ENTITIES = 2
    TAGS = 3
    RELATIONS = 4
    SENTIMENT = 5
    LANGUAGE = 6


class Request(NamedTuple):
    id: str
    title: Optional[str]
    text: Optional[str]
    paraSpecs: Optional[List[ParaSpec]]
    analyses: List[AnalysisType]
    htmlExtractor: str
    language: str
    langDetectPrior: str
    domain: str
    textType: str
    referenceDate: str
    diacritization: str
    returnMentions: bool
    returnItemSentiment: bool
    custom: JsonType

    class Builder:
        def setConfig(self, *,
            analyses: List[AnalysisType] = None,
            htmlExtractor: str = None,
            language: str = None,
            langDetectPrior: str = None,
            domain: str = None,
            textType: str = None,
            referenceDate: str = None,
            # date the time references (e.g., next Tuesday) will be resolved to; formatted as YYYY-MM-DD
            diacritization: str = None,
            returnMentions: bool = None,
            returnItemSentiment: bool = None
        ) -> 'Request.Builder':
            self.analyses = analyses
            self.htmlExtractor = htmlExtractor
            self.language = language
            self.langDetectPrior = langDetectPrior
            self.domain = domain
            self.textType = textType
            self.referenceDate = referenceDate
            self.diacritization = diacritization
            self.returnMentions = returnMentions
            self.returnItemSentiment = returnItemSentiment
            self.custom = {}
            return self

        def setCustom(self, custom: JsonType) -> 'Request.Builder':
            self.custom = custom
            return self

        def build(self, *,
            id: str,
            title: str = None,
            text: str = None,
            paraSpecs: List[ParaSpec] = None,
            language: str = None,
            referenceDate: str = None,
            custom: JsonType = None
        ) -> 'Request':
            if bool(text or title) == bool(paraSpecs):
                raise ValueError('You need to provide title/text or paraSpecs, but not both')

            return Request(
                id=id,
                title=title,
                text=text,
                paraSpecs=paraSpecs,
                analyses=self.analyses if self.analyses else AnalysisType.ALL,
                htmlExtractor=self.htmlExtractor,
                language=language if language else self.language,
                langDetectPrior=self.langDetectPrior,
                domain=self.domain,
                textType=self.textType,
                referenceDate=referenceDate if referenceDate else self.referenceDate,
                diacritization=self.diacritization,
                returnMentions=self.returnMentions,
                returnItemSentiment=self.returnItemSentiment,
                custom=custom if custom else self.custom
            )

    STD_KEYS = {
        'id', 'title', 'text', 'paraSpecs', 'analyses', 'htmlExtractor', 'language', 'langDetectPrior', 'domain',
        'textType', 'referenceDate', 'diacritization', 'returnMentions', 'returnItemSentiment'
    }

    @staticmethod
    def fromDict(raw: JsonType) -> 'Request':
        custom = {key: raw[key] for key in (raw.keys() - Request.STD_KEYS)}
        paraSpecs = raw.get('paraSpecs')

        return Request(
            id=raw['id'],
            title=raw.get('title', None),
            text=raw.get('text', None),
            paraSpecs=[ParaSpec(p['type'], p['text']) for p in paraSpecs] if paraSpecs else None,
            analyses=raw.get('analyses', None),
            htmlExtractor=raw.get('htmlExtractor', None),
            language=raw.get('language', None),
            langDetectPrior=raw.get('langDetectPrior', None),
            domain=raw.get('domain', None),
            textType=raw.get('textType', None),
            referenceDate=raw.get('referenceDate', None),
            diacritization=raw.get('diacritization', 'none'),
            returnMentions=raw.get('returnMentions', False),
            returnItemSentiment=raw.get('returnItemSentiment', False),
            custom=custom
        )

    def toDict(self) -> JsonType:
        return {
            **{
                'id': self.id,
                'title': self.title,
                'text': self.text,
                'paraSpecs': [{'type': p.type, 'text': p.text} for p in self.paraSpecs] if self.paraSpecs else None,
                'analyses': [a.name for a in self.analyses] if self.analyses else None,
                'htmlExtractor': self.htmlExtractor,
                'language': self.language,
                'langDetectPrior': self.langDetectPrior,
                'domain': self.domain,
                'textType': self.textType,
                'referenceDate': self.referenceDate,
                'diacritization': self.diacritization,
                'returnMentions': self.returnMentions,
                'returnItemSentiment': self.returnItemSentiment
            },
            **self.custom
        }
