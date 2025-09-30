***
# BrainRots Project (BSE662)
**Extending the RLWM Model to Ecological Decision-Making: A Bayesian Approach**
***

## Overview

This project explores how working memory (WM) and reinforcement learning (RL) interact to shape human decision-making, using formal computational models and Bayesian inference. We:
- Replicated the RLWM (Reinforcement Learning Working Memory) framework from Anne Collins using Stan.
- Extended the RLWM approach to a dynamic ecological foraging context.
- Developed hierarchical Bayesian models to capture both individual- and group-level variability.

***

## Project Structure

- `stan_models/`: Custom Stan model code for RL, WM, RLWM, and hierarchical RLWM.
- `data/`: Behavioral data for Collins and ecological foraging tasks.
- `notebooks/`: Jupyter notebooks for model fitting, analysis, and visualization.
- `plots/`: Figures and learning curves from empirical and simulated results.
- `env.yml`: Environment file for reproducibility.
- `report.pdf`: Full project report (this document).
- `README.md`: (this file)

***

## Model Overview

**Task 1: Collins Task Implementation**
- Replicates complex learning games where humans must balance WM and RL to learn stimulus-action associations.
- Models:
  - RL2: Pure reinforcement learning.
  - RL6: RL model with varied learning rates for set sizes.
  - RLF: RL with forgetting.
  - WM: Pure working memory.
  - RLWM: Mixture of working memory and RL.

**Task 2: Dynamic Patch Foraging**
- Models adapted for decisions involving exploitation/exploration in dynamic environments with resource depletion and replenishment.
- RL, WM, and RLWM all extended for ecological realism.

**Task 3: Hierarchical Bayesian Extension**
- Hierarchical RLWM to model individual differences, using STAN for full posterior inference.

***

## Key Results

- Bayesian parameter inference produced results closely matching those in the original literature.
- In dynamic foraging, RLWM outperformed pure RL and WM, especially in mimicking nuanced switching behavior and learning curves.
- The influence of WM waned over time/trials as RL took over, reflecting cognitive adaptation.
- Hierarchical models captured population-level trends and meaningful individual differences.

***

## Usage Instructions

1. **Environment Setup**
   ```bash
   conda env create -f env.yml
   conda activate <your-env>
   ```

2. **Model Fitting and Inference**
   - Run the Jupyter notebooks in `notebooks/` to reproduce model fitting, simulations, and figure generation.

3. **Stan Models**
   - Stan code for each model can be found in `stan_models/`.

***

## Results and Plots

Empirical and simulated learning curves, action plots, and fit statistics (AIC, log-likelihood) are provided in the `plots/` directory:
- Learning dynamics for each model.
- Comparison of fitted parameters (WM, RL, mixture weights).
- Hierarchical inferences for cognitive variability.

***

## References

1. Collins AG, Frank MJ (2012). How much of reinforcement learning is working memory, not reinforcement learning?
2. Yoo & Collins (2022). How Working Memory and Reinforcement Learning Are Intertwined.
3. See full report for additional bibliographic details.

***

## Credits

**Faculty Supervisor**: Dr. Arjun Ramakrishnan  
**Mentor**: Kshitij

***

## License

Free for academic use—cite this repo and the above references if reused.

***

**For detailed methods, behavioral analyses, and all figures, see the full PDF report.**
