# storage-app-user

Storage is the base script for JSON and CSV files, where the user executes read, write, add, delete, update and list methods
Movie User Application contains two classes:
MovieApp instance which accepts a storage type in storage.py and its pathway executes storage methods.
UserShell where the user instance is created, checks valid user entries (ID, password pairs), if it is True creates the user files pathway and what type of file its data will be CRAD. It is where the filepath get connect with its user and type.
None of the exceptions in these scripts can interrupt the program flow but UserShell if the user does not want to register or want to exit
