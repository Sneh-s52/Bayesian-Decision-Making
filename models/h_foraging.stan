// Hierarchical RLWM model for Foraging Task
// Adapts logic from single-agent RLWM with flexible subject count

data {
  int<lower=1> N;                      // Number of subjects
  int<lower=1> A;                      // Number of patches/actions
  int<lower=1> Tsubj[N];               // Number of trials per subject
  int<lower=1, upper=A> actions[N, max(Tsubj)];  // Changed to older array syntax
  real<lower=0> rewards[N, max(Tsubj)];          // Changed to older array syntax
}

transformed data {
  vector[A] zero_vec = rep_vector(0.0, A);
}

parameters {
  // Group-level (hyper) parameters
  vector[7] mu_pr;
  vector<lower=0>[7] sigma;

  // Non-centered individual parameters
  vector[N] alpha_pr;
  vector[N] beta_rl_pr;
  vector[N] beta_wm_pr;
  vector[N] forget_pr;
  vector[N] w_pr;
  vector[N] epsilon_pr;
  vector[N] stick_pr;
}

transformed parameters {
  vector<lower=0, upper=1>[N] alpha_rl;
  vector<lower=0>[N] beta_rl;
  vector<lower=0>[N] beta_wm;
  vector<lower=0, upper=1>[N] forget;
  vector<lower=0, upper=1>[N] w;
  vector<lower=0, upper=1>[N] epsilon;
  vector[N] stick;

  for (i in 1:N) {
    alpha_rl[i] = Phi_approx(mu_pr[1] + sigma[1] * alpha_pr[i]);
    beta_rl[i]  = exp(mu_pr[2] + sigma[2] * beta_rl_pr[i]);
    beta_wm[i]  = exp(mu_pr[3] + sigma[3] * beta_wm_pr[i]);
    forget[i]   = Phi_approx(mu_pr[4] + sigma[4] * forget_pr[i]);
    w[i]        = Phi_approx(mu_pr[5] + sigma[5] * w_pr[i]);
    epsilon[i]  = Phi_approx(mu_pr[6] + sigma[6] * epsilon_pr[i]);
    stick[i]    = mu_pr[7] + sigma[7] * stick_pr[i];
  }
}

model {
  // Hyperpriors
  mu_pr ~ normal(0, 1);
  sigma ~ normal(0, 0.2);

  // Individual parameter priors (non-centered)
  alpha_pr   ~ normal(0, 1);
  beta_rl_pr ~ normal(0, 1);
  beta_wm_pr ~ normal(0, 1);
  forget_pr  ~ normal(0, 1);
  w_pr       ~ normal(0, 1);
  epsilon_pr ~ normal(0, 1);
  stick_pr   ~ normal(0, 1);

  for (i in 1:N) {
    vector[A] Q = zero_vec;
    vector[A] WM = zero_vec;
    vector[A] prev_choice_vec = zero_vec;

    for (t in 1:Tsubj[i]) {
      int a = actions[i, t];
      real r = rewards[i, t]; // No scaling as per user specification

      vector[A] logits_rl = beta_rl[i] * Q + stick[i] * prev_choice_vec;
      vector[A] logits_wm = beta_wm[i] * WM + stick[i] * prev_choice_vec;

      real max_rl = max(logits_rl);
      real max_wm = max(logits_wm);
      vector[A] centered_rl = logits_rl - max_rl;
      vector[A] centered_wm = logits_wm - max_wm;

      vector[A] policy_rl = softmax(centered_rl);
      vector[A] policy_wm = softmax(centered_wm);

      vector[A] mix_policy = w[i] * policy_wm + (1 - w[i]) * policy_rl;
      vector[A] final_policy = (1 - epsilon[i]) * mix_policy + epsilon[i]/A;

      target += log(final_policy[a]);

      // RL update
      Q[a] += alpha_rl[i] * (r - Q[a]);

      // WM update
      WM = WM * (1 - forget[i]);
      WM[a] = r;

      // Stickiness update
      prev_choice_vec = zero_vec;
      prev_choice_vec[a] = 1.0;
    }
  }
}

generated quantities {
  real<lower=0, upper=1> mu_alpha_rl = Phi_approx(mu_pr[1]);
  real<lower=0> mu_beta_rl = exp(mu_pr[2]);
  real<lower=0> mu_beta_wm = exp(mu_pr[3]);
  real<lower=0, upper=1> mu_forget = Phi_approx(mu_pr[4]);
  real<lower=0, upper=1> mu_w = Phi_approx(mu_pr[5]);
  real<lower=0, upper=1> mu_epsilon = Phi_approx(mu_pr[6]);
  real mu_stick = mu_pr[7];

  vector[N] log_lik;
  {
    for (i in 1:N) {
      vector[A] Q = zero_vec;
      vector[A] WM = zero_vec;
      vector[A] prev_choice_vec = zero_vec;
      log_lik[i] = 0.0;

      for (t in 1:Tsubj[i]) {
        int a = actions[i, t];
        real r = rewards[i, t];

        vector[A] logits_rl = beta_rl[i] * Q + stick[i] * prev_choice_vec;
        vector[A] logits_wm = beta_wm[i] * WM + stick[i] * prev_choice_vec;

        vector[A] policy_rl = softmax(logits_rl);
        vector[A] policy_wm = softmax(logits_wm);

        vector[A] mix_policy = w[i] * policy_wm + (1 - w[i]) * policy_rl;
        vector[A] final_policy = (1 - epsilon[i]) * mix_policy + epsilon[i]/A;

        log_lik[i] += log(final_policy[a]);

        Q[a] += alpha_rl[i] * (r - Q[a]);
        WM = WM * (1 - forget[i]);
        WM[a] = r;
        prev_choice_vec = zero_vec;
        prev_choice_vec[a] = 1.0;
      }
    }
  }
}
