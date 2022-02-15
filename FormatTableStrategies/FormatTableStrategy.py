from FormatTableStrategies.IterfaceTableStrategy import InterfaceTableFormatStrategy


class FormatTableStrategy(InterfaceTableFormatStrategy):

    def formatLine(self, table_line):
        return table_line.replace(",", "")
