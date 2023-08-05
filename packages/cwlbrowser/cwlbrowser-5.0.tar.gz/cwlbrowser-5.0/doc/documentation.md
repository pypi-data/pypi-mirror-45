# Documentation
Below you will find detailed information about the main functionality of `cwlbrowser`. `cwlbrowser` has two main submodules, namely, `browser` and `similaritychecker`. `browser`deals with loading and browsing workflows whereas `similaritychecker` deals with comparing two workflows and identifying their differences, if any. `cwlbrowser` also has an object known as `Workflow` that has all the attributes of workflows split in `Input` `Output` and `Step` classes. More details here:

## `cwlbrowser.browser` 
### Loading workflows onto the Jupyter notebook
The first step in using the `cwlbrowser` is loading the workflow onto the Jupyter notebook
by calling the function: `load(workflow, link)`. 'workflow' is the GitHub link or local path to the `.cwl` file in question. 'link' is a boolean that indicates to the `load` method whether you are passing a GitHub link or local path to the workflow file. The `load` method returns a `Workflow` object.(More details here)

Example 
```python
import cwlbrowser.browser as b
#loading via GitHub link. 'link' is set to True by default
example = b.load(GITHUB_LINK_TO_WORKFLOW)
#loading local file
example2 = b.load(LOCAL_PATH_TO_FILE, link=False)
```
### Tabular view of workflow 
You can view a tabular representation of a workflow by calling the method `displayTables(workflow, attr)` where 'workflow' is the `Workflow` object and 'attr' is the type of attribute you would like to view.

Example [here:](displayTablesExample.ipynb)

### Graphical view of workflow
You can view a graphical representation of a workflow by calling the method `displayGraph(workflow)` where 'workflow' is a `Workflow` object

Example [here:](displayGraphExample.ipynb)

## `cwlbrowser.similaritychecker`
### Similarity checking and the `SimilarityChecker` object
the `SimilarityChecker` object is used to compare two workflows. Simply instantiate a `SimilarityChecker` object without any parameters and call its instance method `simimlarityCheck(workflow1, workflow2)` to compare two workflow objects. The details of the comparison can be seen by then calling the method `displayStats(similaritychecker)` from the `browser` module  where 'similaritychecker' is the `SimilarityChecker` object. 
Example [here:](comparisonExample.ipynb)


