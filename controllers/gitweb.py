# coding: utf-8

from bottle import route, post, debug, run, redirect
import config, os, re, time
from jade_template import jade_template as _jade_template
from pygit2 import Repository
import pygit2
from functools import *

def path_inits(repo, path):
    p = '/'
    first = True
    for comp in path.split('/'):
        p = os.path.join(p, comp)
        yield first, comp or repo, p
        first = False
        if path == '/':
            break

def jade_template(template_path, **kwargs):
    saved_cwd = os.getcwd()
    os.chdir(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'views'))
    res = _jade_template(template_path, **kwargs)
    os.chdir(saved_cwd)
    return res

@route('/')
@route('/view')
def view_repos():
    repo_list = [dir for dir in os.listdir(config.project_root) if os.path.exists(os.path.join(config.project_root, dir, 'git-daemon-export-ok'))]
    desc_list = []
    for repo in repo_list:
        with open(os.path.join(config.project_root, repo, 'description')) as h:
            desc_list.append(h.read())
    return jade_template('view_repos.jade', repo_list=zip(repo_list, desc_list))

@route('/view/:repo')
def view_repo(repo):
    r = Repository(os.path.join(config.project_root, repo))
    head = r.lookup_reference('HEAD').target
    if head.startswith('refs/heads/'):
        # branch = [ref[11:] for ref in Repository(os.path.join(config.project_root, repo)).listall_references() if ref.startswith('refs/heads/')][0]
        branch = head[11:]
        redirect('/view/%s/tree/branch/%s' % (repo, branch))

@route('/view/:repo/tree/branch/:branch')
@route('/view/:repo/tree/branch/:branch/<filepath:re:.*>')
def view_tree_branch_filepath(repo, branch, filepath=''):
    r = Repository(os.path.join(config.project_root, repo))
    if 'refs/heads/'+branch not in r.listall_references():
        abort(404, 'no such branch')
    c = r[r.lookup_reference('refs/heads/'+branch).oid]
    tree = c.tree
    filepath = re.sub('/+', '/', filepath)
    if not filepath.startswith('/'):
        filepath = '/'+filepath
    if filepath.endswith('/'):
        filepath = filepath[:-1]
    for comp in filepath.split('/'):
        if comp:
            tree = tree[comp].to_object()
    return jade_template('view_tree.jade', repo=repo, branch=branch, filepath=filepath, filepaths=path_inits(repo, os.path.join(filepath)), tree=tree, list=list)


@route('/view/:repo/tree/commit/:commitid')
def view_tree_commit(repo, commitid):
    pass

@route('/view/:repo/commits')
def view_commits(repo):
    r = Repository(os.path.join(config.project_root, repo))
    head = r.lookup_reference('HEAD').target
    redirect('/view/'+repo+'/commit/'+r.lookup_reference(head).hex)

@route('/view/:repo/commit/:commitid')
def view_commit(repo, commitid):
    def get_ancestors(c):
        while True:
            yield c.hex, c.author, time.gmtime(c.commit_time+c.commit_time_offset), c.message
            if c.parents == []:
                break
            c = c.parents[0]
    r = Repository(os.path.join(config.project_root, repo))
    c = r[r.lookup_reference(r.lookup_reference('HEAD').target).oid]
    print c
    return jade_template('view_commit.jade', repo=repo, commits=get_ancestors(c), time=time)


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

