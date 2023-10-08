# OOuserShell
Simple storage methods, in this example, json and csv methods only taken
movieApp class where it calls storage method that had to be defined in userShell class
  it has validate methods preceding possible mistake that interrupts program flow
userShell class creates for every single registry folder that keeps a json dictionary where user name and password saved
then creates userShell instance that keeps user related files path attributes and connect the user to movieApp instance to execute
userShell menu commands

interaction with the user does pass through by userShell class:
constraction attributes are username and password and then it has method that uses instance of storage and movieApp class
