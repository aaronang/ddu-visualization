# Case Study

In this case study, we analyze a couple of real projects, hosted on GitHub, to get a better understanding of DDU.
More specifically, we are interested in how DDU is affected by different kinds of tests, e.g. unit tests, integration tests, acceptance tests, etc., and testing techniques like parameterized testing.
This knowledge could be used to guide developers in writing tests during the software development process.
Ultimately, the goal is to guide the developer in writing tests such that the diagnosability of the test suite improves.

In this section we first discuss the selection criteria that are used for selecting open source projects to analyze.
Secondly, we explain the approach for analyzing the impact of different kinds of tests on DDU.
Then, for each individual term of DDU, i.e. density, diversity, and uniqueness, we give examples to clarify how the term changes with regards to related tests.
Subsequently, we discuss the DDU metric as a whole.
Finally, we conclude this case study with observations and recommendations.


## Selection

The selection of open source projects is done according to the following criteria.

- The project must have a executable test suite.

    To compute the DDU for a software project, we must construct an activity matrix, also known as program spectra.
    The program spectra is constructed by running the test suite and instrumenting the code such that we can keep track of what parts of the code are executed during a program execution.

- The project must use Apache Maven, a software project management and comprehension tool.

    The current tool that instruments the code to construct the activity matrix is implemented as a Maven plugin. Note that the current Maven plugin does not work for all Maven projects, and therefore only projects, that can be analyzed with this plugin, are used.

Based on these requirements, we choose the following open source projects.

- [Commons CSV](commons_csv.md): a library that provides a simple interface for reading and writing CSV files of various types.
- [Commons Text](commons_text.md): a library focused on algorithms working on strings.
- [Guice](guice.md): a lightweight dependency injection framework for Java 6 and above.
- [Jsoup](https://github.com/jhy/jsoup): an API for extracting and manipulating data, using the best of DOM, CSS, and jquery-like methods.


## Approach

To get a better understanding of how DDU varies as a consequence to testing, we use [`ddu-maven-plugin`](https://github.com/aperez/ddu-maven-plugin), written by Perez, to instrument Java code and collect the activity matrix.
The DDU Maven plugin is capable of computing the DDU, however it requires deeper knowledge if we would like to modify the plugin to use different granularities, e.g. class granularity.
Therefore, to compute the DDU, its individual terms, and the metrics for different granularities, we wrote multiple [Python scripts](https://github.com/aaronang/ddu/tree/master/analysis).
Note that class granularity is not supported by `ddu-maven-plugin`; it has support for instrumenting Java at method, block, and line granularity.

With these two tools we collect data such as number of tests, number of unit tests, number of integration test, density, diversity, uniqueness, DDU, and the activity matrix.
Since the definition of unit and integration tests varies from person to person, we use the following simple definition.
At class granularity, a test is considered a unit test when it only covers one class.
Accordingly, a test is considered an integration test when it covers two or more classes.

Then, we analyze the collected data and show examples that illustrate how DDU and its individual terms vary as a consequence to particular kinds of tests.


## Density



## Diversity



## Uniqueness



## DDU