import time
class mockDataTransfer:

    def __init__(self) -> None:
        self.data: str = ""
        self.dataNum: int = 1
    
    def sendData(self) -> str:
        self.dataNum = self.dataNum + 1
        return str(self.dataNum) + "mph"

    def main(self) -> str:
        if self.dataNum < 100:
            self.data = self.sendData()
            return self.data
        else:
            return None
