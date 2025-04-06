# Online Myths on Opioid Use Disorder: A Comparison of Reddit and Large Language Model

## RQ1: Myth classifier

Script for myth classification is ```myth_classification.py```. Comments are provided to include relevant API-related credentials.

* Model: gpt-3.5-turbo
* Prompt: Few-shot with chain-of-thought
* Myth: M1 (```Agonist therapy or medication-assisted treatment for opioid use disorder is merely replacing one drug with another.```)
* Task: To identify human-generated responses (taken from Reddit) promoting the myth

Make relevant changes (detailed in the paper) for other settings.

## RQ2: Social dimension classifiers

We followed the work by *Choi et al. [(2020)](https://dl.acm.org/doi/abs/10.1145/3366423.3380224)* to get classifiers for ```trust```, ```power```, ```conflict```, and ```knowledge``` social dimensions. [[Link-GitHub]](https://github.com/minjechoi/10dimensions).

## RQ2: StorySeeker

We followed the work by *Antoniak et al. [(2024)](https://arxiv.org/abs/2311.09675)* to identify responses containing a ```persuasive storytelling narrative```. [[Link-GitHub]](https://github.com/maria-antoniak/storyseeker).

## References
Choi, M.; Aiello, L. M.; Varga, K. Z.; and Quercia, D. 2020. Ten Social Dimensions of Conversations and Relationships. In Proceedings of The Web Conference (WWW).

Antoniak, M.; Mire, J.; Sap, M.; Ash, E.; and Piper, A. 2024. Where Do People Tell Stories Online? Story Detection Across Online Communities. arXiv:2311.09675
