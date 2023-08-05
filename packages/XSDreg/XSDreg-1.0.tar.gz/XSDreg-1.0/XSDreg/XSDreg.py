import rdflib


class XSDreg:
    """A simple library to obtain regular expressions for xsd types used in rdf"""
    # source of relevant xsd types https://www.w3.org/TR/rdf11-concepts/
    # source: for most regex is https://www.w3.org/TR/xmlschema11-2/#[name]

    def __init__(self):
        self.stringRegex = "[\\s\\S]+"

        self.dateRegex = "-?([1-9][0-9]{3,}|0[0-9]{3})-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])(Z|(\\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00))?"

        self.timeRegex = "(([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9](\\.[0-9]+)?|(24:00:00(\\.0+)?))(Z|(\\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00))?"

        self.dateTimeRegex = "-?([1-9][0-9]{3,}|0[0-9]{3})-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])T(([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9](\\.[0-9]+)?|(24:00:00(\\.0+)?))(Z|(\\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00))?"

        self.dateTimeStampRegex = ".*(Z|(\\+|-)[0-9][0-9]:[0-9][0-9])"

        self.integerRegex = "[\\-+]?[0-9]+"

        self.decimalRegex = "(\\+|-)?([0-9]+(\\.[0-9]*)?|\\.[0-9]+)"

        self.floatRegex = "(\\+|-)?([0-9]+(\\.[0-9]*)?|\\.[0-9]+)([Ee](\\+|-)?[0-9]+)?|(\\+|-)?INF|NaN"

        self.doubleRegex = "(\\+|-)?([0-9]+(\\.[0-9]*)?|\\.[0-9]+)([Ee](\\+|-)?[0-9]+)? |(\\+|-)?INF|NaN"

        self.booleanRegex = "true|false|0|1"

        self.gYearRegex = "-?([1-9][0-9]{3,}|0[0-9]{3})(Z|(\\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00))?"

        self.gMonthRegex = "--(0[1-9]|1[0-2])(Z|(\\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00))?"

        self.gDayRegex = "---(0[1-9]|[12][0-9]|3[01])(Z|(\\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00))?"

        self.gYearMonthRegex = "-?([1-9][0-9]{3,}|0[0-9]{3})-(0[1-9]|1[0-2])(Z|(\\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00))?"

        self.gMonthDayRegex = "--(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])(Z|(\\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00))?"

        self.durationRegex = "-?P[0-9]+Y?([0-9]+M)?([0-9]+D)?(T([0-9]+H)?([0-9]+M)?([0-9]+(\.[0-9]+)?S)?)?"

        self.yearMonthDurationRegex = "-?P((([0-9]+Y)([0-9]+M)?)|([0-9]+M))"

        self.dayTimeDurationRegex = "[^YM]*[DT].*"

        self.byteRegex = "-128|[\\-+]?12[0-7]|[\\-+]?1[01][0-9]|[\\-+]?[1-9][0-9]|[\\-+]?[0-9]"

        self.shortRegex = "0|-32768|[\\-+]?3276[0-7]|[\\-+]?327[0-5][0-9]|[\\-+]?32[0-6][0-9]{2}|[\\-+]?3[01][0-9]{3}|[\\-+]?[12][0-9]{4}|[\\-+]?[1-9][0-9]{0,3}"

        self.intRegex = "-2147483648|0|[\\-+]?[01][0-9]{9}|[\\-+]?20[0-9]{8}|[\\-+]?21[0-3][0-9]{7}|[\\-+]?214[0-6][0-9]{6}|[\\-+]?2147[0-3][0-9]{5}|[\\-+]?21474[0-7][0-9]{4}|[\\-+]?214748[012][0-9]{3}|[\\-+]?2147483[0-5][0-9]{2}|[\\-+]?21474836[0-3][0-9]|[\\-+]?214748364[0-8]|[\\-+]?[1-9][0-9]{0,8}"

        self.longRegex = "-9223372036854775808|0|[\\-+]?[1-8][0-9]{18}|[\\-+]?9[01][0-9]{17}|[\\-+]?92[01][0-9]{16}|[\\-+]?922[012][0-9]{15}|[\\-+]?9223[012][0-9]{14}|[\\-+]?92233[0-6][0-9]{13}|[\\-+]?922337[01][0-9]{12}|[\\-+]?92233720[012][0-9]{10}|[\\-+]?922337203[0-5][0-9]{9}|[\\-+]?9223372036[0-7][0-9]{8}|[\\-+]?92233720368[0-4][0-9]{7}|[\\-+]?922337203685[0-3][0-9]{6}|[\\-+]?9223372036854[0-6][0-9]{5}|[\\-+]?92233720368547[0-6][0-9]{4}|[\\-+]?922337203685477[0-4][0-9]{3}|[\\-+]?9223372036854775[0-7][0-9]{2}|[\\-+]?922337203685477580[0-8]{2}|[\\-+]?[1-9][0-9]{0,17}"

        self.unsignedByteRegex = "0|+?[01][0-9]{2}|+?2[0-4][0-9]|+?25[0-5]|+?[1-9][0-9]{0,1}"

        self.unsignedShortRegex = "0|+?[0-5][0-9]{4}|+?6[0-4][0-9]{3}|+?65[0-4][0-9]{2}|+?655[012][0-9]|+?6553[0-5]|+?[1-9][0-9]{0,3}"

        self.unsignedIntRegex = "0|+?[0-3][0-9]{9}|+?4[01][0-9]{8}|+?42[0-8][0-9]{7}|+?429[0-3][0-9]{6}|+?4294[0-8][0-9]{5}|+?42949[0-5][0-9]{4}|+?429496[0-6][0-9]{3}|+?4294967[01][0-9]{2}|+?42949672[0-8][0-9]|+?429496729[0-5]|[\-+]?[1-9][0-9]{0,8}"

        self.unsignedLongRegex = "0|+?1[0-7][0-9]{18}|+?18[0-3][0-9]{17}|+?184[0-3][0-9]{16}|+?1844[0-5][0-9]{15}|+?18446[0-6][0-9]{14}|+?184467[0-3][0-9]{13}|+?1844674[0-3][0-9]{12}|+?184467440[0-6][0-9]{10}|+?1844674407[012][0-9]{9}|+?18446744073[0-6][0-9]{8}|+?1844674407370[0-8][0-9]{6}|+?18446744073709[0-4][0-9]{5}|+?184467440737095[0-4][0-9]{4}|+?18446744073709550[0-9]{3}|+?18446744073709551[0-5][0-9]{2}|+?1844674407370955160[0-9]|+?1844674407370955161[0-5]|[\-+]?[1-9][0-9]{0,18}"

        self.positiveIntegerRegex = "+?[1-9][0-9]*"

        self.nonNegativeIntegerRegex = "0|+?[1-9][0-9]*"

        self.negativeIntegerRegex = "-?[1-9][0-9]*"

        self.nonPositiveIntegerRegex = "0|-?[1-9][0-9]*"

        self.hexBinaryRegex = "([0-9a-fA-F]{2})*"

        self.base64BinaryRegex = "((([A-Za-z0-9+/] ?){4})*(([A-Za-z0-9+/] ?){3}[A-Za-z0-9+/]|([A-Za-z0-9+/] ?){2}[AEIMQUYcgkosw048] ?=|[A-Za-z0-9+/] ?[AQgw] ?= ?=))?"

        self.xsd = rdflib.Namespace('http://www.w3.org/2001/XMLSchema#')

        self.map = {
                    str(self.xsd.string) : self.stringRegex,
                    str(self.xsd.boolean) : self.booleanRegex,
                    str(self.xsd.decimal) : self. decimalRegex,
                    str(self.xsd.integer) : self.integerRegex,
                    str(self.xsd.double) : self.doubleRegex,
                    str(self.xsd.float) : self.floatRegex,
                    str(self.xsd.date) : self.dateRegex,
                    str(self.xsd.time) : self.timeRegex,
                    str(self.xsd.dateTime) : self.dateTimeRegex,
                    str(self.xsd.dateTimeStamp) : self.dateTimeStampRegex,
                    str(self.xsd.gYear) : self.gYearRegex,
                    str(self.xsd.gMonth) : self.gMonthRegex,
                    str(self.xsd.gDay) :self.gDayRegex,
                    str(self.xsd.gYearMonth) : self.gYearMonthRegex,
                    str(self.xsd.gMonthDay) : self.gMonthDayRegex,
                    str(self.xsd.duration) : self.durationRegex,
                    str(self.xsd.yearMonthDuration) : self.yearMonthDurationRegex,
                    str(self.xsd.dayTimeDuration) : self.dayTimeDurationRegex,
                    str(self.xsd.byte) : self.byteRegex,
                    str(self.xsd.short) : self.shortRegex,
                    str(self.xsd.int) : self.intRegex,
                    str(self.xsd.long) : self.longRegex,
                    str(self.xsd.unsignedByte) : self.unsignedByteRegex,
                    str(self.xsd.unsignedShort) : self.unsignedShortRegex,
                    str(self.xsd.unsignedInt) : self.unsignedIntRegex,
                    str(self.xsd.unsignedLong) : self.unsignedLongRegex,
                    str(self.xsd.positiveInteger) : self.positiveIntegerRegex,
                    str(self.xsd.nonNegativeInteger) : self.nonNegativeIntegerRegex,
                    str(self.xsd.negativeInteger) : self.negativeIntegerRegex,
                    str(self.xsd.nonPositiveInteger) : self.nonPositiveIntegerRegex,
                    str(self.xsd.hexBinary) : self.hexBinaryRegex,
                    str(self.xsd.base64BinaryRegex) : self.base64BinaryRegex,
               }

    def getRegex(self, xsdURI):
        return self.map[xsdURI]
