setwd("~/Documents/courses/6th Sem/BSE662- Decision Making and The Brain/Project/models")

# Load required packages
library(hBayesDM)
library(rstan)  # Add this to access stan() function

# Set parallel processing options for Stan
options(mc.cores = parallel::detectCores())
rstan_options(auto_write = TRUE)

# Load raw data from original CSV
data <- read.csv("Foraging_data.csv")

# Map subject names to numeric IDs
data$subjID <- as.numeric(factor(data$Name))

# Convert Patch (0-based) to 1-based
data$choice <- data$Patch + 1

# Store reward directly
data$reward <- data$Reward

# List of unique subjects
subj_list <- sort(unique(data$subjID))
N <- length(subj_list)

# Number of patches (actions)
A <- max(data$choice)

# Trials per subject
Tsubj <- sapply(subj_list, function(sid) sum(data$subjID == sid))
max_T <- max(Tsubj)

# Initialize action and reward matrices with correct dimensions
actions <- matrix(0, nrow = N, ncol = max_T)
rewards <- matrix(0, nrow = N, ncol = max_T)

# Fill the matrices
for (i in 1:N) {
  sid <- subj_list[i]
  subj_data <- subset(data, subjID == sid)
  trials_for_subj <- nrow(subj_data)
  actions[i, 1:trials_for_subj] <- subj_data$choice
  rewards[i, 1:trials_for_subj] <- subj_data$reward
}

# Create Stan data structure
stan_data <- list(
  N = N,
  A = A,
  Tsubj = Tsubj,
  actions = actions,
  rewards = rewards
)

# Write to .Rdump file if needed
rstan::stan_rdump(names(stan_data), file = "foraging_data_hBayesDM.txt", envir = list2env(stan_data))

stan_file_path <- "~/Documents/courses/6th Sem/BSE662- Decision Making and The Brain/Project/models/h_foraging.stan"
stan_content <- readLines(stan_file_path)
writeLines(stan_content, stan_file_path)

# Run Stan model
tryCatch({
  fit <- stan(
    file = "h_foraging.stan",
    data = stan_data,
    chains = 4,
    iter = 2000,
    warmup = 1000,
    cores = 4,
    seed = 42
  )
  
  # Save the fitted model
  saveRDS(fit, file = "h_foraging_fit.rds")
  
  # Examine model outputs
  print(fit, pars = c("mu_alpha_rl", "mu_beta_rl", "mu_beta_wm", "mu_forget", "mu_w", "mu_epsilon", "mu_stick"))
  
  # Plot diagnostics
  traceplot(fit, pars = c("mu_alpha_rl", "mu_beta_rl", "mu_beta_wm", "mu_forget", "mu_w", "mu_epsilon", "mu_stick"))
  
  # Check Rhat values (should be close to 1)
  rhat_values <- rstan::summary(fit)$summary[, "Rhat"]
  rhat_issues <- which(rhat_values > 1.1)
  if(length(rhat_issues) > 0) {
    cat("Warning: Some parameters have Rhat > 1.1, indicating potential convergence issues\n")
  } else {
    cat("All Rhat values look good (< 1.1)\n")
  }
  
  # Extract individual parameters
  params <- rstan::extract(fit)
  
}, error = function(e) {
  cat("Error running Stan model:\n")
  print(e)
  cat("\nChecking data structure compatibility with model...\n")
  
  # Print data structure for debugging
  cat("Actions matrix dimensions:", dim(actions), "\n")
  cat("Rewards matrix dimensions:", dim(rewards), "\n")
  cat("Tsubj vector:", Tsubj, "\n")
})

