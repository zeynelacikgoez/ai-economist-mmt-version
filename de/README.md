# Foundation: Ein Wirtschaftssimulation-Framework MMT-Version

Dieses Repository enthält eine Implementierung von Foundation, einem Framework für flexible, modulare und kombinierbare Umgebungen, die **sozioökonomische Verhaltensweisen und Dynamiken in einer Gesellschaft mit Agenten und Regierungen modellieren**. Die ursprüngliche Implementierung von Foundation ging davon aus, dass die heutige Geldpolitik metallisch ist. Dies entspricht jedoch nicht der Realität, da das Bretton-Woods-System 1971 endete, als die Vereinigten Staaten ihren Goldstandard aufgaben. Ab diesem Zeitpunkt waren die Rahmenbedingungen für eine chartalistische Geldpolitik gegeben. Die Implementierung wird in dieser Version von Foundation vervollständigt.

Foundation bietet eine [Gym](https://gym.openai.com/)-Style API:

- `reset`: setzt den Zustand der Umgebung zurück und gibt die Beobachtung zurück.
- `step`: lässt die Umgebung um einen Zeitschritt voranschreiten und gibt das Tupel *(Beobachtung, Belohnung, fertig, Info)* zurück.

Diese Simulation kann in Verbindung mit Verstärkungslernen verwendet werden, um optimale Wirtschaftspolitiken zu erlernen, wie in den folgenden Papieren detailliert beschrieben:

**[The AI Economist: Verbesserung von Gleichheit und Produktivität mit KI-getriebenen Steuerpolitiken](https://arxiv.org/abs/2004.13332)**,
*Stephan Zheng, Alexander Trott, Sunil Srinivasa, Nikhil Naik, Melvin Gruesbeck, David C. Parkes, Richard Socher.*

**[The AI Economist: Optimales wirtschaftspolitisches Design durch zweistufiges tiefes Verstärkungslernen](https://arxiv.org/abs/2108.02755)**
*Stephan Zheng, Alexander Trott, Sunil Srinivasa, David C. Parkes, Richard Socher.*

**[Aufbau einer Grundlage für datengetriebenes, interpretierbares und robustes Politikdesign mit dem AI Economist](https://arxiv.org/abs/2108.02904)**
*Alexander Trott, Sunil Srinivasa, Douwe van der Wal, Sebastien Haneuse, Stephan Zheng.*

Wenn Sie diesen Code in Ihrer Forschung verwenden, zitieren Sie uns bitte mit diesem BibTeX-Eintrag:

```
@misc{2004.13332,
 Author = {Stephan Zheng, Alexander Trott, Sunil Srinivasa, Nikhil Naik, Melvin Gruesbeck, David C. Parkes, Richard Socher},
 Title = {The AI Economist: Verbesserung von Gleichheit und Produktivität mit KI-getriebenen Steuerpolitiken},
 Year = {2020},
 Eprint = {arXiv:2004.13332},
}
```

Weitere Informationen und Kontext finden Sie unter:

- [Die Website des AI Economist](https://www.einstein.ai/the-ai-economist)
- [Blog: Der AI Economist: Verbesserung von Gleichheit und Produktivität mit KI-getriebenen Steuerpolitiken](https://blog.einstein.ai/the-ai-economist/)
- [Blog: Der AI Economist Moonshot](https://blog.einstein.ai/the-ai-economist-moonshot/)
- [Blog: Die Webdemo des AI Economist zur COVID-19-Fallstudie](https://blog.einstein.ai/ai-economist-covid-case-study-ethics/)
- [Webdemo: Die ethische Bewertung des AI Economist zur Gestaltung von KI-Politik und COVID-19-Fallstudie](https://einstein.ai/the-ai-economist/ai-policy-foundation-and-covid-case-study)

## Simulationskarten: Ethikbewertung und beabsichtigte Verwendung

Bitte sehen Sie sich unsere [Simulationskarte](https://github.com/salesforce/ai-economist/blob/master/Simulation_Card_Foundation_Economic_Simulation_Framework.pdf) für eine Überprüfung der beabsichtigten Verwendung und ethischen Bewertung unseres Frameworks an.

Bitte sehen Sie sich unsere [COVID-19 Simulationskarte](https://github.com/salesforce/ai-economist/blob/master/COVID-19_Simulation-Card.pdf) für eine Überprüfung der ethischen Aspekte der Pandemiesimulation (und wie sie für COVID-19 angepasst wurde) an.

---

## Treten Sie uns auf Slack bei

Wenn Sie daran interessiert sind, dieses Framework zu erweitern, über maschinelles Lernen für die Wirtschaft zu diskutieren und an Forschungsprojekten zu arbeiten:

- treten Sie unserem Slack-Kanal [aieconomist.slack.com](https://aieconomist.slack.com) über diesen [Einladungslink](https://join.slack.com/t/aieconomist/shared_invite/zt-g71ajic7-XaMygwNIup~CCzaR1T0wgA) bei, oder
- schreiben Sie uns eine E-Mail an ai.economist@salesforce.com.

## Installationsanweisungen

Um zu beginnen, müssen Sie Python 3.7+ installiert haben.

### Verwendung von pip

Verwenden Sie einfach den Python-Paketmanager:

```python
pip install ai-economist
```

### Installation aus der Quelle

1. Klonen Sie dieses Repository auf Ihren lokalen Rechner:

  ```
   git clone www.github.com/salesforce/ai-economist
   ```

2. Erstellen Sie eine neue conda-Umgebung (unten als "ai-economist" bezeichnet - ersetzen Sie sie durch einen anderen Namen) und aktivieren Sie sie

  ```pyfunctiontypecomment
   conda create --name ai-economist python=3.7 --yes
   conda activate ai-economist
   ```

3. Entweder

   a) Bearbeiten Sie die PYTHONPATH, um das Verzeichnis ai-economist einzubeziehen
  ```
   export PYTHONPATH=<lokaler Pfad zu ai-economist>:$PYTHONPATH
   ```

   ODER

   b) Installieren Sie es als bearbeitbares Python-Paket
  ```pyfunctiontypecomment
   cd ai-economist
   pip install -e .
   ```

Nützlicher Tipp: Für schnellen Zugriff fügen Sie Folgendes zu Ihrer ~/.bashrc oder ~/.bash_profile hinzu:

```pyfunctiontypecomment
alias aiecon="conda activate ai-economist; cd <lokaler Pfad zu ai-economist>"
```

Sie können dann einfach `aiecon` ausführen, um die conda-Umgebung zu aktivieren.

### Testen Ihrer Installation

Um Ihre Installation zu testen, versuchen Sie:

```
conda activate ai-economist
python -c "import ai_economist"
```

## Erste Schritte

Um sich mit Foundation vertraut zu machen, werfen Sie einen Blick auf die Tutorials im Ordner `tutorials`. Sie können diese Notebooks interaktiv in Ihrem Browser auf Google Colab ausführen.

### Multi-Agenten-Simulationen

- [economic_simulation_basic](https://www.github.com/salesforce/ai-economist/blob/master/tutorials/economic_simulation_basic.ipynb) ([Probieren Sie dies auf Colab aus](http://colab.research.google.com/github/salesforce/ai-economist/blob/master/tutorials/economic_simulation_basic.ipynb)!): Zeigt, wie man mit der Simulation interagiert und sie visualisiert.
- [economic_simulation_advanced](https://www.github.com/salesforce/ai-economist/blob/master/tutorials/economic_simulation_advanced.ipynb) ([Probieren Sie dies auf Colab aus](http://colab.research.google.com/github/salesforce/ai-economist/blob/master/tutorials/economic_simulation_advanced.ipynb)!): Erklärt, wie Foundation mit zusammensetzbaren und flexiblen Bausteinen aufgebaut ist.
- [optimal_taxation_theory_and_simulation](https://github.com/salesforce/ai-economist/blob/master/tutorials/optimal_taxation_theory_and_simulation.ipynb) ([Probieren Sie dies auf Colab aus](https://colab.research.google.com/github/salesforce/ai-economist/blob/master/tutorials/optimal_taxation_theory_and_simulation.ipynb)!): Demonstriert, wie wirtschaftliche Simulationen verwendet werden können, um das Problem der optimalen Besteuerung zu untersuchen.
- [covid19_and_economic_simulation](https://www.github.com/salesforce/ai-economist/blob/master/tutorials/covid19_and_economic_simulation.ipynb) ([Probieren Sie dies auf Colab aus](http://colab.research.google.com/github/salesforce/ai-economist/blob/master/tutorials/covid19_and_economic_simulation.ipynb)!): Stellt eine Simulation zur COVID-19-Pandemie und Wirtschaft vor, die zur Untersuchung verschiedener Gesundheits- und Wirtschaftspolitiken verwendet werden kann.



### Multi-Agenten-Training
- [multi_agent_gpu_training_with_warp_drive](https://github.com/salesforce/ai-economist/blob/master/tutorials/multi_agent_gpu_training_with_warp_drive.ipynb) ([Probieren Sie dies auf Colab aus](http://colab.research.google.com/github/salesforce/ai-economist/blob/master/tutorials/multi_agent_gpu_training_with_warp_drive.ipynb)!): Stellt unser Multi-Agenten-Verstärkungslernframework [WarpDrive](https://arxiv.org/abs/2108.13976) vor, das wir dann verwenden, um die COVID-19- und Wirtschaftssimulation zu trainieren.
- [multi_agent_training_with_rllib](https://github.com/salesforce/ai-economist/blob/master/tutorials/multi_agent_training_with_rllib.ipynb) ([Probieren Sie dies auf Colab aus](http://colab.research.google.com/github/salesforce/ai-economist/blob/master/tutorials/multi_agent_training_with_rllib.ipynb)!): Zeigt, wie man verteiltes Multi-Agenten-Verstärkungslernen mit [RLlib](https://docs.ray.io/en/latest/rllib/index.html) durchführt.
- [two_level_curriculum_training_with_rllib](https://github.com/salesforce/ai-economist/blob/master/tutorials/two_level_curriculum_learning_with_rllib.md): Beschreibt, wie man zweistufiges Curriculum-Training mit [RLlib](https://docs.ray.io/en/latest/rllib/index.html) implementiert.

Um diese Notebooks *lokal* auszuführen, benötigen Sie [Jupyter](https://jupyter.org). Siehe [https://jupyter.readthedocs.io/en/latest/install.html](https://jupyter.readthedocs.io/en/latest/install.html) für Installationsanweisungen und [(https://jupyter-notebook.readthedocs.io/en/stable/](https://jupyter-notebook.readthedocs.io/en/stable/) für Beispiele, wie man mit Jupyter arbeitet.

## Struktur des Codes

- Die Simulation befindet sich im Ordner `ai_economist/foundation`.

Das Code-Repository ist in folgende Komponenten gegliedert:

| Komponente | Beschreibung |
| --- | --- |
| [base](https://www.github.com/salesforce/ai-economist/blob/master/ai_economist/foundation/base) | Enthält Basisklassen, die erweitert werden können, um Agenten, Komponenten und Szenarien zu definieren. |
| [agents](https://www.github.com/salesforce/ai-economist/blob/master/ai_economist/foundation/agents) | Agenten repräsentieren wirtschaftliche Akteure in der Umgebung. Derzeit haben wir mobile Agenten (die Arbeiter repräsentieren) und einen sozialen Planer (der eine Regierung repräsentiert). |
| [entities](https://www.github.com/salesforce/ai-economist/blob/master/ai_economist/foundation/entities) | Endogene und exogene Komponenten der Umgebung. Endogene Entitäten umfassen Arbeit, während exogene Entitäten Wahrzeichen (wie Wasser und Gras) und sammelbare Ressourcen (wie Holz und Stein) umfassen. |
| [components](https://www.github.com/salesforce/ai-economist/blob/master/ai_economist/foundation/components) | Komponenten werden verwendet, um bestimmte Dynamiken in einer Umgebung hinzuzufügen. Sie fügen auch Aktionsräume hinzu, die definieren, wie Agenten über die Komponente mit der Umgebung interagieren können. |
| [scenarios](https://www.github.com/salesforce/ai-economist/blob/master/ai_economist/foundation/scenarios) | Szenarien setzen Komponenten zusammen, um die Dynamik der Welt zu definieren. Es berechnet auch Belohnungen und stellt Zustände zur Visualisierung zur Verfügung. |

- Die Datensätze (einschließlich der Echtzeitdaten zu COVID-19) befinden sich im Ordner `ai_economist/datasets`.

## Veröffentlichungen und Mitwirkung

- Bitte lassen Sie uns wissen, wenn Sie auf Fehler stoßen, indem Sie ein GitHub-Issue einreichen.
- Wir schätzen alle Ihre Beiträge. Wenn Sie planen, neue Komponenten, Szenarien, Entitäten oder etwas anderes beizutragen, sehen Sie bitte unsere [Richtlinien für Beiträge](https://www.github.com/salesforce/ai-economist/blob/master/CONTRIBUTING.md).


## Änderungsprotokoll

Für die vollständige Veröffentlichungsgeschichte, siehe [CHANGELOG.md](https://www.github.com/salesforce/ai-economist/blob/master/CHANGELOG.md).

## Lizenz

Foundation und der AI Economist sind unter der [BSD-3-Lizenz](LICENSE.txt) veröffentlicht.
