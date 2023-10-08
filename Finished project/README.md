# OOuserShell
Simple storage methods, in this example, JSON and CSV methods only taken
movieApp class where it calls the storage method that had to be defined in userShell class
  it has validated methods preceding possible mistake that interrupts program flow
userShell class creates for every single registry folder that keeps a JSON dictionary where user name and password saved
then creates userShell instance that keeps user-related file path attributes and connects the user to movieApp instance to execute
userShell menu commands

interaction with the user does pass through by userShell class:
construction attributes are username and password and then it has a method that uses the instance of storage and movieApp class
