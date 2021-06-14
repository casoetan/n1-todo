# Contributing

To contribute to the project, follow the [setup guide](./README.md#Setup)

## Steps to contribute

- Create an issue and discuss your changes first
- When changes have been agreed, go ahead and makes your changes within your branch (use issue id for branch naming)
- Write tests to cover features introduced
- Make sure all tests pass
- Format your code properly
- Update tag (project uses semantic versioning)
    - Patch tag if bug fix
    - Minor tag if adding a new feature without breaking changes
    - Major tag if your changes will introduce a breaking change
- Add changes made to [changelog](./CHANGELOGS.md)
- Submit a PR against the develop branch
- Once PR is approved merge into develop and create a release branch from develop with your changes
- Submit PR with release branch targetting main
- Once approved, merge into main
