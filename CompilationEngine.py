from JackTokenizer import JackTokenizer, KEYWORD_TYPE, SYMBOL_TYPE, \
    INTEGER_CONST_TYPE, STRING_CONST_TYPE, IDENTIFIER_TYPE, TAG_CLOSER, TAG_SUFFIX, TAG_PREFIX

OP_LIST = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
UNARY_OP_LIST = ['-', '~']
CLASS_TAG = "class"
CLASS_VAR_TAG = "classVarDec"
SUBROUTINE_BODY_TAG = "subroutineBody"
PARAMETERS_LIST_TAG = "parameterList"
CLASS_VAR_DEC_KEYWORDS = ["field, static"]
SUBROUTINE_DEC_TAG = "subroutineDec"
SUBROUTINE_DEC_KEYWORDS = ['constructor', 'function', 'method']
TYPE_LIST = ["int", "char", "boolean"]
ADDITIONAL_VAR_OPTIONAL_MARK = ","
TAG_OPENER = "\t"


class CompilationEngine:

    def __init__(self, input_stream, output_stream):
        """
        Creates a new compilation engine with the
        given input and output. The next routine
        called must be compileClass().
        """
        self.__prefix = ""
        self.__tokenizer = JackTokenizer(input_stream)
        self.__output_stream = output_stream

    def compile(self):
        """
        Compiles the whole file
        :return: True iff the file was compiled successfully
        """
        return self.__compile_class()

    def __compile_class(self):
        """
        Compiles a complete class
        :return: True iff the class was compiled successfully
        """
        # writes to the file the class tag and increment the prefix tabs
        self.__output_stream.write(self.__create_tag(CLASS_TAG))

        # checks for the next parts of the class and writes them to the file
        self.__check_keyword_symbol(KEYWORD_TYPE)  # "class"
        self.__check_keyword_symbol(IDENTIFIER_TYPE)  # className
        self.__check_keyword_symbol(SYMBOL_TYPE)  # "{"
        # if not self.__tokenizer.has_more_tokens():
        #     return False  # should have more tokens
        #
        # # checks for optional classVerDec and subroutineDec
        # self.__tokenizer.advance()
        while self.__compile_class_var_dec():  # and self.__tokenizer.has_more_tokens():
            # self.__tokenizer.advance()
            continue
        while self.__compile_subroutine(False):  # and self.__tokenizer.has_more_tokens():
            # self.__tokenizer.advance()
            continue

        # if not self.__tokenizer.has_more_tokens():
        #     return False  # should have more tokens
        # else:
        self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # block closer "}"

        # writes to the file the class end tag
        self.__output_stream.write(self.__create_tag(CLASS_TAG, TAG_CLOSER))

    def __compile_class_var_dec(self, make_advance=True):
        """
        Compiles a static declaration or a field declaration
        :param: make_advance: boolean parameter- should make advance before the first call or not. Default value is True
        :return: True iff there was a valid class var declaration
        """
        if not self.__check_keyword_symbol(KEYWORD_TYPE, CLASS_VAR_DEC_KEYWORDS, make_advance):
            # It is not a class var dec
            return False

        # writes to the file the class tag and increment the prefix tabs
        self.__output_stream.write(self.__create_tag(CLASS_VAR_TAG))

        self.__check_type()
        self.__check_keyword_symbol(IDENTIFIER_TYPE)  # varName
        while self.__check_keyword_symbol(SYMBOL_TYPE, [ADDITIONAL_VAR_OPTIONAL_MARK]):  # "," more varName
            self.__check_keyword_symbol(IDENTIFIER_TYPE)  # varName

        self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # ";"

        # writes to the file the class end tag
        self.__output_stream.write(self.__create_tag(CLASS_VAR_TAG, TAG_CLOSER))
        return True

    def __compile_subroutine(self, make_advance=True):
        """

        :param: make_advance: boolean parameter- should make advance before the first call or not. Default value is True
        :return: True iff there was a valid subroutine declaration
        """
        if not self.__check_keyword_symbol(KEYWORD_TYPE, SUBROUTINE_DEC_KEYWORDS, make_advance):
            # It is not a subroutine
            return False

        # writes to the file the class tag and increment the prefix tabs
        self.__output_stream.write(self.__create_tag(SUBROUTINE_DEC_TAG))

        if not self.__check_keyword_symbol(KEYWORD_TYPE):  # not void
            self.__check_type()
        self.__check_keyword_symbol(IDENTIFIER_TYPE)  # subroutineName
        self.__check_keyword_symbol(SYMBOL_TYPE)  # "("
        if self.__compile_parameter_list():
            self.__check_keyword_symbol(SYMBOL_TYPE)  # ")"
        else:  # advance was made in the compile_parameter_list without use
            self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # ")"
        self.__compile_subroutine_body()

        # writes to the file the class end tag
        self.__output_stream.write(self.__create_tag(SUBROUTINE_DEC_TAG, TAG_CLOSER))
        return True

    def __compile_subroutine_body(self):
        # writes to the file the class tag and increment the prefix tabs
        self._output_stream.write(self._create_tag(SUBROUTINE_BODY_TAG))

        self.__check_keyword_symbol(SYMBOL_TYPE)  # '{'

        # writes to the file the class end tag
        self._output_stream.write(self._create_tag(SUBROUTINE_BODY_TAG, TAG_CLOSER))

    def __compile_parameter_list(self):
        if not self.__check_type():
            # It is not a parameter list
            return False

        # writes to the file the class tag and increment the prefix tabs
        self.__output_stream.write(self.__create_tag(PARAMETERS_LIST_TAG))

        if not self.__check_keyword_symbol(KEYWORD_TYPE):  # not void
            self.__check_type()
        self.__check_keyword_symbol(IDENTIFIER_TYPE)  # subroutineName
        self.__check_keyword_symbol(SYMBOL_TYPE)  # "("
        if self.__compile_parameter_list():
            self.__check_keyword_symbol(SYMBOL_TYPE)  # ")"
        else:  # advance was made in the compile_parameter_list without use
            self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # ")"
        self.__compile_subroutine_body()

        # writes to the file the class end tag
        self.__output_stream.write(self.__create_tag(PARAMETERS_LIST_TAG, TAG_CLOSER))
        return True

    def __compile_var_dec(self):
        # writes to the file the class tag and increment the prefix tabs
        self._output_stream.write(self._create_tag(SUBROUTINE_BODY_TAG))

        # checks if there is a
        if not self.__check_keyword_symbol(KEYWORD_TYPE):  # 'var'
            return False

        self.__check_type()
        self.__check_keyword_symbol(IDENTIFIER_TYPE)  # variableName
        while self.__check_keyword_symbol(SYMBOL_TYPE, [ADDITIONAL_VAR_OPTIONAL_MARK]):
            self.__check_keyword_symbol(IDENTIFIER_TYPE)

        self.__check_keyword_symbol(SYMBOL_TYPE, make_advance=False)  # ';'

        # writes to the file the class end tag
        self._output_stream.write(self._create_tag(SUBROUTINE_BODY_TAG, TAG_CLOSER))
        return True

    def __compile_statements(self):
        pass

    def __compile_do(self):
        pass

    def __compile_let(self):
        pass

    def __compile_while(self):
        pass

    def __compile_return(self):
        pass

    def __compile_if(self):
        pass

    def __compile_expression(self):
        pass

    def __compile_term(self):
        pass

    def __compile_expression_list(self):
        pass

    def __check_keyword_symbol(self, token_type, value_list=None, make_advance=True, write_to_file=True):
        """
        checks if the current token is from token_type (which is keyword or symbol), and it's value is one of the
        given optional values (in the value_list). If so, writes the token string to the output file
        :param token_type: the wanted type of the current token: keyword or symbol
        :param value_list: a list of optional values for the current token
        :return: True if the current token is from Keyword type, and it's value exists in the keyword list,
          and false otherwise
        """
        if make_advance:
            if self.__tokenizer.has_more_tokens():
                self.__tokenizer.advance()
            else:
                return False
        if self.__tokenizer.get_token_type() == token_type:
            if value_list is None or self.__tokenizer.get_value() in value_list:
                if write_to_file:
                    self.__output_stream.write(self.__prefix + self.__tokenizer.get_token_string())
                return True

        return False

    def __check_type(self):
        """
        checks if the current token is a type. If so, writes the token to the stream
        :return: true iff the current token is a type
        """
        # checks for builtin types
        if self.__check_keyword_symbol(KEYWORD_TYPE, TYPE_LIST):
            return True
        # checks for user-defined class types
        if not self.__check_keyword_symbol(IDENTIFIER_TYPE, False):
            return False

        return True

    def __check_op(self):
        """
        :return: true iff the current token is a symbol containing an operation
        """
        return self.__check_keyword_symbol(OP_LIST, SYMBOL_TYPE)

    def __check_unary_op(self):
        """
        :return: true iff the current token is a symbol containing an unary operation
        """
        return self.__check_keyword_symbol(UNARY_OP_LIST, SYMBOL_TYPE)

    def __create_tag(self, tag, closer=''):
        """
        Creates the type tag in its format
        :param tag: The actual tag
        :param closer: the closer note if there should be one. Otherwise it has default empty value
        :return: the type tag
        """
        if closer:
            # the closer is not empty - decrementing it and set the prefix to be after the changing
            self.__prefix = self.__prefix[:-len(TAG_OPENER)]
            prefix = self.__prefix
        else:
            # the closer is empty - saves the current prefix before incrementing it for the next tag
            prefix = self.__prefix
            self.__prefix += TAG_OPENER

        return prefix + TAG_PREFIX + closer + tag + TAG_SUFFIX
