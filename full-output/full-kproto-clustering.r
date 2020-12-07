library("clustMixType")

# load in the data
original <- read.csv('csv-files/full_log_normalized.csv')

# drop the first three columns (and education)
df <- original[ , !(names(original) %in% c("X", "nb_id", "repo_id", "is_education"))]

# kproto clustering for no repo dups
Es <- numeric(10)
for (i in 1:10) {
    kpres <- kproto(df, k = i, nstart = 10)
    Es[i] <- kpres$tot.withinss
}

# create plot and save to file
jpeg("figures/log_normalized_clusters.jpg", width = 350, height = 350)
plot(1:10, Es, type = "b", ylab = "Objective Function", xlab = "# Clusters",
    main = "Log Normalized - Scree Plot")
dev.off()

