# gitbump

It's just little enhancement of simple but looking good: 
https://gitlab.com/threedotslabs/ci-scripts/blob/master/common/gen-semver

Basically automate semantic versioning in Git repo using tags.

By default scripts updated **patch** number, you can update **minor** or **major**
by using following commands in commit message:

 * bump: major
 * bump: minor
 * bump: patch (default)

WARNING: Order matters !

Additionaly if you setup tag by hand, this script won't increment tag.
