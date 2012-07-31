# coding: utf-8

from bottle import route, post, debug, run
import config, os
from jade_template import jade_template as _jade_template

def jade_template(filepath, **kwargs):
    saved_cwd = os.getcwd()
    os.chdir(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'views'))
    res = _jade_template(filepath, **kwargs)
    os.chdir(saved_cwd)
    return res

@route('/view')
def view_repo_list():
    repo_list = [dir for dir in os.listdir(config.project_root) if os.path.exists(os.path.join(config.project_root, dir, 'git-daemon-export-ok'))]
    print [dir for dir in os.listdir(config.project_root)]
    return jade_template('view.jade', repo_list=repo_list)

@route('/view/:repo')
def view_repo(repo):
    pass

@route('/view/:repo/tree/branch/:branch/:filepath')
def view_tree_branch_filepath(repo, branch, filepath):
    pass


@route('/view/:repo/tree/commit/:commitid')
def view_tree_commit(repo, commitid):
    pass

@route('/view/:repo/commit/:commitid')
def view_commit(repo, commitid):
    pass


@route('/view/:repo/tag')
def view_tag_list(repo):
    pass

@route('/view/:repo/tag/:tag')
def view_tag(repo):
    pass

@route('/view/:repo/tag/:tag/tgz')
def view_tag_tgz(repo, tag):
    pass

@route('/view/:repo/tag/:tag/zip')
def view_tag_zipb(repo, tag):
    pass


@route('/admin/:repo')
def admin_repo(repo):
    pass

@route('/admin')
def admin():
    pass

@route('/admin/create')
def admin_create():
    pass

@post('/admin/create')
def admin_create_post():
    pass

@route('/admin/:repo/delete')
def admin_delete(repo):
    pass

@route('/admin/:repo/rename')
def admin_rename(repo):
    pass

@route('/admin/:repo/public')
def admin_public(repo):
    pass

@route('/admin/:repo/private')
def admin_private(repo):
    pass

debug()
run(host='localhost', port=8000)

