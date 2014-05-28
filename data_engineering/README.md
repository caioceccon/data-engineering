[ ![Codeship Status](https://codeship.io/projects/eae09450-c835-0131-a153-3281d6cd49ef/status?branch=master)](https://www.codeship.io/projects/22274)

# Billing TXT Parser
To run this project follow the instructions bellow.

## Instaling and Running Instructions.
1. Install the requirements with the commands `pip install -r requirements.txt`.
1. Run the sync command `./manage.py syncdb` and follow the instruction to create the admin user.
1. Then start the server with the command `./manage.py runserver`.
1. To run the tests run `./manage.py test sales`.


## Usage Instruction
1. Login in the django admin site, access the admin interface and submit the billing file on the billing area.
1. OBS: The project have been fully covered with tests. 
