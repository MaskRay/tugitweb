# coding: utf-8

from bottle import route


@route('/view')
def repolist():
    pass

@route('/view/:repo')
def repoview(repo):
    pass

@route('/view/:repo/tree/branch/:branch/:filepath')
def viewcodebybranch(repo, branch, filepath):
    pass


@route('/view/:repo/tree/commit/:commitid')
def viewcodebycommit(repo, commitid):
    pass

@route('/view/:repo/commit/:commitid')
def viewcommit(repo, commitid):
    pass

@route('/view/:repo/tags')
def viewtags(repo):
    pass

@route('/view/:repo/tags/tgz/:tag')
def tgztags(repo, tag):
    pass

@route('/view/:repo/tags/zip/:tag')
def ziptags(repo, tag):
    pass

@route('/admin/:repo')
def adminrepo(repo):
    pass

@route('/admin')
def adminhome():
    pass

@route('/admin/create')
def admincreate():
    pass

@route('/admin/create', method = 'POST')
def admincreate_post():
    pass

@route('/admin/:repo/delete')
def admindelete(repo):
    pass

@route('/admin/:repo/rename')
def adminrename(repo):
    pass

@route('/admin/:repo/public')
def adminpublich(repo):
    pass

@route('/admin/:repo/private')
def adminprivate(repo):
    pass

