from fontTools import ttLib
from hellbox import Chute, Hellbox


class InsertDummyDsig(Chute):
    """InsertDummyDsig adds a valid DSIG table with no signatures."""

    def run(self, files):
        return [self._process(file) for file in files]

    def _process(self, file):
        Hellbox.info(f"Updating DSIG: {file.basename}")

        copy = file.copy()

        font = ttLib.TTFont(copy.content_path)
        font.tables["DSIG"] = self._create_signature()
        font.save(copy.content_path)

        return copy

    def _create_signature(self):
        table = ttLib.newTable("DSIG")
        table.ulVersion = 1
        table.usFlag = 0
        table.usNumSigs = 0
        table.signatureRecords = []
        return table
