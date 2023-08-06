from git import Repo
import git

student_id = "xoxo"

"""curr_repo_path = 'student_repos/' + student_id
student_repo = Repo.clone_from('https://retting.ii.uib.no/' + student_id + '/inf101.v19.sem2', curr_repo_path)
#Repo.init(curr_repo_path)"""

curr_repo_path = 'student_repos/' + student_id
student_repo = Repo.init(curr_repo_path)
try:
    origin = student_repo.create_remote('origin', 'https://retting.ii.uib.no/' + student_id + '/inf101.v19.sem2')
    # origin = student_repo.create_remote('origin', 'https://retting.ii.uib.no/'+ student_id +'/python-pushing-est') # Testing purposes

except git.exc.GitCommandError:
    print("You have already cloned this repo in here!")
    origin = student_repo.remote('origin')

# TESTS AND SHIT
assert origin.exists()
assert origin == student_repo.remotes.origin == student_repo.remotes['origin']
try:
    origin.fetch()
except git.exc.GitCommandError:
    if not student_id:
        print("Didn't find any student ID.")
    else:
        print("{} is not a valid student ID.".format(student_id))

    print("Going to next sheet...")


