# coding: utf-8

from bottle import route, post, debug, run, redirect, static_file
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

views_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'views')

def jade_template(template_path, **kwargs):
    saved_cwd = os.getcwd()
    os.chdir(views_dir)
    res = _jade_template(template_path, **kwargs)
    os.chdir(saved_cwd)
    return res

@route('/css/<filepath:path>')
def css(filepath):
    return static_file(filepath, root=views_dir+'/css')

@route('/js/<filepath:path>')
def js(filepath):
    return static_file(filepath, root=views_dir+'/js')

@route('/')
@route('/view')
def view_repos():
    repo_list = [dir for dir in os.listdir(config.project_root) if os.path.exists(os.path.join(config.project_root, dir, 'git-daemon-export-ok'))]
    desc_list = []
    for repo in repo_list:
        with open(os.path.join(config.project_root, repo, 'description')) as h:
            desc_list.append(h.read())
    return jade_template('view_repos.jade', repo_list=zip(repo_list, desc_list))

# Tree

@route('/view/:repo')
@route('/view/:repo/')
def view_repo(repo):
    r = Repository(os.path.join(config.project_root, repo))
    head = r.lookup_reference('HEAD').target
    return view_tree_commit_filepath(repo, r.lookup_reference(head).hex, '')

@route('/view/:repo/tree/commit/:commitid')
@route('/view/:repo/tree/commit/:commitid/<filepath:re:.*>')
def view_tree_commit_filepath(repo, commitid, filepath='', base_url=None):
    r = Repository(os.path.join(config.project_root, repo))
    tree = r[unicode(commitid)].tree

    filepath = re.sub('/+', '/', filepath)
    if not filepath.startswith('/'):
        filepath = '/'+filepath
    if filepath.endswith('/'):
        filepath = filepath[:-1]

    for comp in filepath.split('/'):
        if comp:
            tree = tree[comp].to_object()
    di = last_change=last_change_for_each_entry(r[unicode(commitid)])
    return jade_template('view_tree.jade', repo=repo, commitid=commitid, filepath=filepath, filepaths=path_inits(repo, os.path.join(filepath)), tree=tree, list=list, base_url=base_url or '/view/'+repo+'/tree/commit/'+commitid, last_change=last_change_for_each_entry(r[unicode(commitid)]))

@route('/view/:repo/branches')
def view_branches(repo):
    r = Repository(os.path.join(config.project_root, repo))
    tags = [(ref[11:], r.lookup_reference(ref).hex) for ref in r.listall_references() if ref.startswith('refs/heads/')]
    return jade_template('view_tags.jade', repo=repo, tags=tags)

def last_change_for_each_entry(commit):
    mapping = {e.oid: commit for e in commit.tree}
    c = commit
    print commit.tree
    while c.parents:
        c = c.parents[0]
        for e in c.tree:
            if mapping.has_key(e.oid):
                mapping[e.oid] = c
    res = {}
    for e in commit.tree:
        c = mapping[e.oid]
        iso8601 = time.strftime('%FT%T', time.localtime(c.commit_time))
        hh, mm = c.commit_time_offset//60, c.commit_time_offset%60
        if hh < 0 and mm > 0:
            hh += 1
            mm = 60-mm
        iso8601_offset = '%+03d%02d' % (hh, mm)
        res[e.name] = (iso8601, iso8601_offset, c, c)
    return res

@route('/view/:repo/tree/branch/:branch')
@route('/view/:repo/tree/branch/:branch/<filepath:re:.*>')
def view_tree_branch_filepath(repo, branch, filepath=''):
    r = Repository(os.path.join(config.project_root, repo))
    if 'refs/heads/'+branch not in r.listall_references():
        abort(404, 'no such branch')
    c = r.lookup_reference('refs/heads/'+branch).hex
    return view_tree_commit_filepath(repo, c, filepath, base_url='/view/'+repo+'/branch/'+branch)

@route('/view/:repo/commits')
def view_commits(repo):
    r = Repository(os.path.join(config.project_root, repo))
    head = r.lookup_reference('HEAD').target
    redirect('/view/'+repo+'/commit/'+r.lookup_reference(head).hex)

def get_ancestors(c):
    while True:
        iso8601 = time.strftime('%FT%T', time.localtime(c.commit_time))
        hh, mm = c.commit_time_offset//60, c.commit_time_offset%60
        if hh < 0 and mm > 0:
            hh += 1
            mm = 60-mm
        iso8601_offset = '%+03d%02d' % (hh, mm)
        yield c.hex, c.author, iso8601, iso8601_offset, c.message
        if c.parents == []:
            break
        c = c.parents[0]

@route('/view/:repo/commit/:commitid')
def view_commit(repo, commitid):
    r = Repository(os.path.join(config.project_root, repo))
    return jade_template('view_commit.jade', repo=repo, commits=get_ancestors(r[unicode(commitid)]), time=time)


@route('/view/:repo/tags')
def view_tags(repo):
    r = Repository(os.path.join(config.project_root, repo))
    tags = [(ref[10:], r[r[r.lookup_reference(ref).oid].target].hex) for ref in r.listall_references() if ref.startswith('refs/tags/')]
    return jade_template('view_tags.jade', repo=repo, tags=tags)

@route('/view/:repo/tag/:tag')
def view_tag(repo, tag):
    r = Repository(os.path.join(config.project_root, repo))
    if 'refs/tags/'+tag not in r.listall_references():
        abort(404, 'no such tag')
    commitid = r[r[r.lookup_reference('refs/tags/'+tag).oid].target]
    return jade_template('view_tag.jade', repo=repo, commits=get_ancestors(commitid), time=time, focus_commit=commitid)

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

