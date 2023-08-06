from stanfordnlp.server.client import *
import requests


class Token(object):

    def __init__(self, doc, index, char_start, char_end):
        self.index = index
        self.doc = doc
        self.char_start = char_start
        self.char_end = char_end

    def __repr__(self):
        return '({0},{1},{2})'.format(
            self.char_start,
            self.char_end,
            self.doc.text[self.char_start:self.char_end])


class Span(object):

    def __init__(self, doc, start, end):
        self.doc = doc
        self.start = start
        self.end = end

    @property
    def char_start(self):
        return self.doc.tokens[self.start].char_start

    @property
    def char_end(self):
        return self.doc.tokens[self.end - 1].char_end

    @property
    def text(self):
        return self.doc.text[self.char_start:self.char_end]

    def __repr__(self):
        return '({0},{1},{2})'.format(
            self.char_start,
            self.char_end,
            self.doc.text[self.char_start:self.char_end])


class Phrase(Span):

    def __init__(self, doc, start, end, tag):
        super().__init__(doc, start, end)
        self.tag = tag

    def __repr__(self):
        return '({0},{1},{2},{3})'.format(self.char_start, self.char_end,
                                          self.text,
                                          self.tag)


class Sentence(Span):

    def __init__(self, doc, start, end, index, constituency):
        self.index = index
        super().__init__(doc, start, end)
        self._extract_phrases(constituency)

    def _extract_phrases(self, constituency):
        tags = []
        phrase_starts = []
        tok_idx = self.start
        i = 0
        length = len(constituency)
        self.phrases = []
        while i < length:
            if constituency[i] == '(':
                i += 1
                prev = i
                while not str.isspace(constituency[i]):
                    i += 1
                tags.append(constituency[prev:i])
                phrase_starts.append(tok_idx)
            elif str.isspace(constituency[i]):
                i += 1
            elif constituency[i] == ')':
                pstart = phrase_starts.pop()
                tag = tags.pop()
                phrase = Phrase(self.doc, pstart, tok_idx, tag)
                self.phrases.append(phrase)
                i += 1
            else:
                prev = i
                while constituency[i] not in '()' \
                        and not str.isspace(constituency[i]):
                    i += 1
                tok_idx += 1
                tok_text = constituency[prev:i]


class Document(object):

    def __init__(self, text, resp):
        assert isinstance(resp, dict)
        self.text = text
        self.tokens = []
        self.sentences = []

        for jsent in resp['sentences']:
            for jtoken in jsent['tokens']:
                tok = Token(self, len(self.tokens),
                            jtoken['characterOffsetBegin'],
                            jtoken['characterOffsetEnd'])
                self.tokens.append(tok)
            sentence = Sentence(self, len(self.tokens) - len(jsent['tokens']),
                                len(self.tokens),
                                len(self.sentences), jsent['parse'])
            self.sentences.append(sentence)

    @property
    def phrases(self):
        for sent in self.sentences:
            for phrase in sent.phrases:
                yield phrase


class LanguageCoreNLPClient(CoreNLPClient):
    '''
    This class inherits from CoreNLPClient to support language dependant
    parsing.
    '''

    def _request(self, buf, properties, language='en'):
        """Send a request to the CoreNLP server.

        :param (str | unicode) text: raw text for the CoreNLPServer to parse
        :param (dict) properties: properties that the server expects
        :return: request result
        """
        self.ensure_alive()

        try:
            input_format = properties.get("inputFormat", "text")
            if input_format == "text":
                ctype = "text/plain; charset=utf-8"
            elif input_format == "serialized":
                ctype = "application/x-protobuf"
            else:
                raise ValueError("Unrecognized inputFormat " + input_format)

            r = requests.post(self.endpoint,
                              params={'properties': str(properties),
                                      'pipelineLanguage': language},
                              data=buf, headers={'content-type': ctype},
                              timeout=(self.timeout * 2) / 1000)
            r.raise_for_status()
            return r
        except requests.HTTPError as e:
            if r.text == "CoreNLP request timed out. " \
                         "Your document may be too long.":
                raise TimeoutException(r.text)
            else:
                raise AnnotationException(r.text)

    def annotate(self, text, annotators=None, properties=None, language='en'):
        """Send a request to the CoreNLP server.

        :param (str | unicode) text: raw text for the CoreNLPServer to parse
        :param (list | string) annotators: list of annotators to use
        :param (dict) properties: properties that the server expects
        :return: request result
        """
        # set properties for server call
        if properties is None:
            properties = self.default_properties
            properties.update({
                'annotators': ','.join(annotators or self.default_annotators),
                'inputFormat': 'text',
                'outputFormat': 'json'
            })
        elif "annotators" not in properties:
            properties.update({'annotators': ','.join(
                annotators or self.default_annotators)})

        if language == 'zh':
            text = text.replace('(', '（') \
                    .replace(')', '）') \
                    .replace(',', '，')

        # make the request
        r = self._request(text.encode('utf-8'), properties, language)
        return Document(text, r.json())
