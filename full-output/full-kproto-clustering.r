library("clustMixType")

# load in the data
md_original <- read.csv('csv-files/full_markdown_group.csv')
no_md_original <- read.csv('csv-files/full_no_markdown_group.csv') 

# drop the first three columns
md_df <- md_original[ , !(names(md_original) %in% c("X", "nb_id", "repo_id"))]
no_md_df <- no_md_original[ , !(names(no_md_original) %in% c("X", "nb_id", "repo_id"))]

# kproto clustering for md group
Es <- numeric(10)
for (i in 1:10) {
    kpres <- kproto(md_df, k = i, nstart = 10)
    Es[i] <- kpres$tot.withinss
}

# create plot and save to file
jpeg("markdown_group_clusters_8.jpg", width = 350, height = 350)
plot(1:10, Es, type = "b", ylab = "Objective Function", xlab = "# Clusters",
    main = "Markdown Group - Scree Plot") 
dev.off()

# kproto clustering for no md group
Es <- numeric(10)
for (i in 1:10) {
    kpres <- kproto(no_md_df, k = i, nstart = 10)
    Es[i] <- kpres$tot.withinss
}

# create plot and save to file
jpeg("no_markdown_group_clusters_8.jpg", width = 350, height = 350)
plot(1:10, Es, type = "b", ylab = "Objective Function", xlab = "# Clusters",
    main = "No Markdown Group - Scree Plot") 
dev.off()
