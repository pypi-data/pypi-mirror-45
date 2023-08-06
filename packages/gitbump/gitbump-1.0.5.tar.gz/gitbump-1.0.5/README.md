# gitbump

It's just little enhancement of simple but looking good: 
https://gitlab.com/threedotslabs/ci-scripts/blob/master/common/gen-semver

Basically automate semantic versioning in Git repo using tags.

Prerequistes:
 * Setup **CI_REPOSITORY_URL** variable  (GitLab default)


By default scripts updated **patch** number, you can update **minor** or **major**
by using following commands in commit message:

 * #bump_major
 * #bump_minor
 * #bump_patch (default)

WARNING: Order matters !