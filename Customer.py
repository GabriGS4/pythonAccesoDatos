class Customer:
    headings = ['ID', 'Name', 'Bill Address', 'Phone', 'Email', 'Pos']
    fields = {
        '-ID-': 'Customer ID:',
        '-Name-': 'Customer Name:',
        '-Bill-': 'Billing Address:',
        '-Phone-': 'Phone:',
        '-Email-': 'Email:',
        '-PosFile-': 'Position into File'
    }

    def __init__(self, ID, name, bill, phone, email, posFile):
        self.ID = ID
        self.name = name
        self.bill = bill
        self.phone = phone
        self.email = email
        self.posFile = posFile
        self.erased = False

    def __eq__(self, oC):
        return oC.posFile == self.posFile

    def __str__(self):
        return f"{self.ID} {self.name} {self.bill} {self.phone} {self.email} {self.posFile}"

    def __repr__(self):
        return f"Customer(ID={self.ID}, name={self.name}, bill={self.bill}, phone={self.phone}, email={self.email}, posFile={self.posFile})"

    def customerinPos(self, pos):
        return str(self.posFile) == str(pos)

    def setCustomer(self, name, bill, phone, email):
        self.name = name
        self.bill = bill
        self.phone = phone
        self.email = email
