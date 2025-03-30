import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { styles } from '../styles';
import { SectionWrapper } from '../hoc';
import { fadeIn, textVariant, staggerContainer } from '../utils/motion';
import { github } from '../assets';
import { getKey } from '../config/keys';

const GitHubContributions = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [stats, setStats] = useState({
    contributions: 0,
    commits: 0,
    pullRequests: 0,
    codeReviews: 0,
    repositories: 0,
    languages: [],
    topLanguages: [],
    currentStreak: 0,
    longestStreak: 0,
    totalStars: 0
  });

  useEffect(() => {
    const fetchGitHubStats = async () => {
      try {
        const token = getKey('GITHUB_TOKEN');

        if (!token) {
          throw new Error(
            'GitHub token not configured.'
          );
        }

        // Updated query to get more accurate stats and streak information
        const query = `
          query {
            user(login: "ersachinsaurav") {
              contributionsCollection {
                totalCommitContributions
                totalPullRequestContributions
                totalIssueContributions
                contributionCalendar {
                  totalContributions
                  weeks {
                    contributionDays {
                      contributionCount
                      date
                    }
                  }
                }
                restrictedContributionsCount
                totalRepositoryContributions
                totalPullRequestReviewContributions
                totalPullRequestContributions
                totalRepositoriesWithContributedCommits
                totalRepositoriesWithContributedPullRequests
              }
              repositories(first: 100) {
                totalCount
                nodes {
                  name
                  stargazerCount
                  defaultBranchRef {
                    target {
                      ... on Commit {
                        history(first: 100) {
                          totalCount
                          pageInfo {
                            hasNextPage
                            endCursor
                          }
                        }
                      }
                    }
                  }
                }
              }
              privateRepos: repositories(first: 100, privacy: PRIVATE) {
                totalCount
              }
              publicRepos: repositories(first: 100, privacy: PUBLIC) {
                totalCount
              }
              allRepos: repositories(first: 100) {
                nodes {
                  languages(first: 10) {
                    nodes {
                      name
                      color
                    }
                  }
                  primaryLanguage {
                    name
                    color
                  }
                }
              }
            }
          }
        `;

        const response = await fetch('https://api.github.com/graphql', {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ query })
        });

        if (!response.ok) {
          if (response.status === 401) {
            throw new Error(
              'GitHub token is invalid or expired.'
            );
          }
          throw new Error(
            'GitHub stats are temporarily unavailable.'
          );
        }

        const data = await response.json();

        if (data.errors) {
          throw new Error(
            'GitHub API Error: ' + data.errors[0].message
          );
        }

        const userData = data.data.user;
        const contributions = userData.contributionsCollection;

        // Calculate total commits from repositories
        const totalCommits = userData.repositories.nodes.reduce((acc, repo) => {
          if (repo.defaultBranchRef?.target?.history?.totalCount) {
            return acc + repo.defaultBranchRef.target.history.totalCount;
          }
          return acc;
        }, 0);

        // Use the contributions collection count as it's more accurate
        const finalTotalCommits = contributions.totalCommitContributions;

        // Prepare days in chronological order for streak calculations
        const allDays = [];
        contributions.contributionCalendar.weeks.forEach(week => {
          week.contributionDays.forEach(day => {
            allDays.push(day);
          });
        });

        // Sort days from oldest to newest
        allDays.sort((a, b) => new Date(a.date) - new Date(b.date));

        // Get today's date at midnight for comparison
        const today = new Date();
        today.setHours(0, 0, 0, 0);

        // Get date from 30 days ago for current streak calculation
        const thirtyDaysAgo = new Date(today);
        thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
        thirtyDaysAgo.setHours(0, 0, 0, 0);

        // Get date from 1 year ago for longest streak calculation
        const oneYearAgo = new Date(today);
        oneYearAgo.setFullYear(oneYearAgo.getFullYear() - 1);
        oneYearAgo.setHours(0, 0, 0, 0);

        // Current streak (longest streak in last 30 days)
        let currentStreak = 0;
        let tempCurrentStreak = 0;

        // Longest streak (longest streak in last year)
        let longestStreak = 0;
        let tempLongestStreak = 0;

        // Loop through all days to calculate both streaks
        for (let i = 0; i < allDays.length; i++) {
          const day = allDays[i];
          const date = new Date(day.date);
          date.setHours(0, 0, 0, 0);

          // Skip days older than one year ago
          if (date < oneYearAgo) {
            continue;
          }

          if (day.contributionCount > 0) {
            // For longest streak (within 1 year)
            tempLongestStreak++;
            if (tempLongestStreak > longestStreak) {
              longestStreak = tempLongestStreak;
            }

            // For current streak (within 30 days)
            if (date >= thirtyDaysAgo) {
              tempCurrentStreak++;
              if (tempCurrentStreak > currentStreak) {
                currentStreak = tempCurrentStreak;
              }
            }
          } else {
            // Reset streaks when a day has no contributions
            tempLongestStreak = 0;

            // Only reset current streak if within 30 days
            if (date >= thirtyDaysAgo) {
              tempCurrentStreak = 0;
            }
          }
        }

        // Make sure we include the streak if it's ongoing on the last day
        if (tempLongestStreak > longestStreak) {
          longestStreak = tempLongestStreak;
        }

        if (tempCurrentStreak > currentStreak) {
          currentStreak = tempCurrentStreak;
        }

        // Process languages and filter out unwanted ones
        const languageMap = new Map();
        userData.allRepos.nodes.forEach(repo => {
          // Add primary language
          if (repo.primaryLanguage?.name && !['Hack', 'Other', 'EJS'].includes(repo.primaryLanguage.name)) {
            languageMap.set(repo.primaryLanguage.name, (languageMap.get(repo.primaryLanguage.name) || 0) + 1);
          }

          // Add other languages
          repo.languages.nodes.forEach(lang => {
            if (!['Hack', 'Other', 'EJS'].includes(lang.name)) {
              languageMap.set(lang.name, (languageMap.get(lang.name) || 0) + 1);
            }
          });
        });

        // Add React.js and Node.js if not present
        if (!languageMap.has('React')) {
          languageMap.set('React', 1);
        }
        if (!languageMap.has('Node.js')) {
          languageMap.set('Node.js', 1);
        }

        // Sort languages by usage and get top 8
        const topLanguages = Array.from(languageMap.entries())
          .sort((a, b) => b[1] - a[1])
          .slice(0, 8)
          .map(([name, count]) => ({ name, count }));

        // Calculate total stars
        const totalStars = userData.repositories.nodes.reduce((acc, repo) => {
          return acc + (repo.stargazerCount || 0);
        }, 0);

        setStats({
          contributions: contributions.contributionCalendar.totalContributions,
          commits: finalTotalCommits,
          pullRequests: contributions.totalPullRequestContributions,
          codeReviews: contributions.totalPullRequestReviewContributions,
          repositories: userData.publicRepos.totalCount + userData.privateRepos.totalCount,
          languages: Array.from(languageMap.entries()).map(([name, count]) => ({ name, count })),
          topLanguages,
          currentStreak,
          longestStreak,
          totalStars
        });
        setLoading(false);
      } catch (error) {
        setError(error.message);
        setLoading(false);
      }
    };

    fetchGitHubStats();
  }, []);

  const renderStats = () => {
    if (loading) {
      return <div className="text-white text-center">Loading contributions...</div>;
    }

    if (error) {
      return (
        <div className="text-center">
          <div className="text-red-500 mb-4">{error}</div>
          <div className="grid grid-cols-3 gap-4 mb-4">
            <div className="bg-[#1d1836] p-4 rounded-xl opacity-50">
              <p className="text-white text-lg font-semibold">-</p>
              <p className="text-white text-sm">Total Activities</p>
            </div>
            <div className="bg-[#1d1836] p-4 rounded-xl opacity-50">
              <p className="text-white text-lg font-semibold">-</p>
              <p className="text-white text-sm">Code Commits</p>
            </div>
            <div className="bg-[#1d1836] p-4 rounded-xl opacity-50">
              <p className="text-white text-lg font-semibold">-</p>
              <p className="text-white text-sm">Pull Requests</p>
            </div>
          </div>
          <p className="text-white text-sm mt-2">
            <span className="text-[#ff6b6b]">⚠️</span> Stats temporarily unavailable
          </p>
        </div>
      );
    }

    return (
      <div className="mt-4 text-center">
        <p className="text-white text-sm mb-4">
          <span className="text-[#ff6b6b]">🔥</span> Stats shown are from {new Date(new Date().setFullYear(new Date().getFullYear() - 1)).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })} to {new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}
        </p>

        <motion.div
          variants={staggerContainer()}
          initial="hidden"
          whileInView="show"
          viewport={{ once: false, amount: 0.25 }}
          className="grid grid-cols-3 gap-4 mb-4"
        >
          <motion.div
            variants={fadeIn('right', 'spring', 0.2, 0.75)}
            whileHover={{
              scale: 1.05,
              backgroundColor: '#2d1f4a',
              transition: { duration: 0.2 }
            }}
            className="bg-[#1d1836] p-4 rounded-xl cursor-pointer"
          >
            <p className="text-white text-lg font-semibold">{stats.contributions}</p>
            <p className="text-white text-sm">Total Contributions</p>
          </motion.div>
          <motion.div
            variants={fadeIn('right', 'spring', 0.3, 0.75)}
            whileHover={{
              scale: 1.05,
              backgroundColor: '#2d1f4a',
              transition: { duration: 0.2 }
            }}
            className="bg-[#1d1836] p-4 rounded-xl cursor-pointer"
          >
            <p className="text-white text-lg font-semibold">{stats.commits}</p>
            <p className="text-white text-sm">Code Commits</p>
          </motion.div>
          <motion.div
            variants={fadeIn('right', 'spring', 0.4, 0.75)}
            whileHover={{
              scale: 1.05,
              backgroundColor: '#2d1f4a',
              transition: { duration: 0.2 }
            }}
            className="bg-[#1d1836] p-4 rounded-xl cursor-pointer"
          >
            <p className="text-white text-lg font-semibold">{stats.pullRequests}</p>
            <p className="text-white text-sm">Pull Requests</p>
          </motion.div>
        </motion.div>

        <motion.div
          variants={staggerContainer()}
          initial="hidden"
          whileInView="show"
          viewport={{ once: false, amount: 0.25 }}
          className="grid grid-cols-3 gap-4 mb-4"
        >
          <motion.div
            variants={fadeIn('right', 'spring', 0.5, 0.75)}
            whileHover={{
              scale: 1.05,
              backgroundColor: '#2d1f4a',
              transition: { duration: 0.2 }
            }}
            className="bg-[#1d1836] p-4 rounded-xl cursor-pointer"
          >
            <p className="text-white text-lg font-semibold">{stats.codeReviews}</p>
            <p className="text-white text-sm">Code Reviews</p>
          </motion.div>
          <motion.div
            variants={fadeIn('right', 'spring', 0.6, 0.75)}
            whileHover={{
              scale: 1.05,
              backgroundColor: '#2d1f4a',
              transition: { duration: 0.2 }
            }}
            className="bg-[#1d1836] p-4 rounded-xl cursor-pointer"
          >
            <p className="text-white text-lg font-semibold">{stats.currentStreak}</p>
            <p className="text-white text-sm">30-Day Best</p>
          </motion.div>
          <motion.div
            variants={fadeIn('right', 'spring', 0.7, 0.75)}
            whileHover={{
              scale: 1.05,
              backgroundColor: '#2d1f4a',
              transition: { duration: 0.2 }
            }}
            className="bg-[#1d1836] p-4 rounded-xl cursor-pointer"
          >
            <p className="text-white text-lg font-semibold">{stats.longestStreak}</p>
            <p className="text-white text-sm">Longest Streak</p>
          </motion.div>
        </motion.div>

        <motion.div
          variants={staggerContainer()}
          initial="hidden"
          whileInView="show"
          viewport={{ once: false, amount: 0.25 }}
          className="grid grid-cols-3 gap-4 mb-4"
        >
          <motion.div
            variants={fadeIn('right', 'spring', 0.8, 0.75)}
            whileHover={{
              scale: 1.05,
              backgroundColor: '#2d1f4a',
              transition: { duration: 0.2 }
            }}
            className="bg-[#1d1836] p-4 rounded-xl cursor-pointer"
          >
            <p className="text-white text-lg font-semibold">{stats.repositories}</p>
            <p className="text-white text-sm">Total Repositories</p>
          </motion.div>
          <motion.div
            variants={fadeIn('right', 'spring', 0.9, 0.75)}
            whileHover={{
              scale: 1.05,
              backgroundColor: '#2d1f4a',
              transition: { duration: 0.2 }
            }}
            className="bg-[#1d1836] p-4 rounded-xl cursor-pointer"
          >
            <p className="text-white text-lg font-semibold">{stats.languages.length}</p>
            <p className="text-white text-sm">Languages</p>
          </motion.div>
          <motion.div
            variants={fadeIn('right', 'spring', 1, 0.75)}
            whileHover={{
              scale: 1.05,
              backgroundColor: '#2d1f4a',
              transition: { duration: 0.2 }
            }}
            className="bg-[#1d1836] p-4 rounded-xl cursor-pointer"
          >
            <p className="text-white text-lg font-semibold">{stats.totalStars}</p>
            <p className="text-white text-sm">Total Stars</p>
          </motion.div>
        </motion.div>

        {stats.topLanguages.length > 0 && (
          <motion.div
            variants={fadeIn('up', 'spring', 1.1, 0.75)}
            initial={{ opacity: 1 }}
            className="mt-4"
          >
            <h4 className="text-white text-lg font-semibold mb-2">Top Languages</h4>
            <div className="flex flex-wrap justify-center gap-2">
              {stats.topLanguages.map((lang, index) => (
                <motion.div
                  key={index}
                  variants={fadeIn('up', 'spring', 1.2 + index * 0.1, 0.75)}
                  initial={{ opacity: 1 }}
                  whileHover={{
                    scale: 1.1,
                    backgroundColor: '#2d1f4a',
                    transition: { duration: 0.2 }
                  }}
                  className="bg-[#1d1836] px-3 py-1 rounded-full cursor-pointer"
                >
                  <span className="text-white text-sm">{lang.name}</span>
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}

        <motion.p
          variants={fadeIn('up', 'spring', 1.3, 0.75)}
          initial={{ opacity: 1 }}
          className="text-white text-sm mt-4"
        >
          <span className="text-[#ff6b6b]">✨</span> Many more contributions in private repositories
        </motion.p>
      </div>
    );
  };

  return (
    <>
      <motion.div variants={textVariant()}>
        <p className={styles.sectionSubText}>My Activity</p>
        <h2 className={styles.sectionHeadText}>GitHub Contributions</h2>
      </motion.div>

      <motion.div
        variants={fadeIn('', '', 0.1, 1)}
        className="mt-4 flex flex-col items-center">
        <div className="w-full bg-tertiary p-8 rounded-2xl relative">
          <div className="flex items-center justify-between mb-6">
            <img src={github} alt="github" className="w-12 h-12" />
            <h3 className="text-white text-[24px] font-bold">GitHub Activity</h3>
          </div>

          <div className="relative z-10">
            {renderStats()}
          </div>

          <div className="flex justify-end mt-8 relative z-10">
            <motion.a
              href="https://github.com/ersachinsaurav"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 text-[#915eff] text-sm hover:text-[#ff6b6b] transition-all duration-300 hover:scale-105 cursor-pointer"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <span className="flex items-center gap-2">
                Visit my GitHub profile
                <motion.span
                  animate={{ x: [0, 5, 0] }}
                  transition={{ duration: 1.5, repeat: Infinity }}
                >
                  →
                </motion.span>
              </span>
            </motion.a>
          </div>
        </div>
      </motion.div>
    </>
  );
};

export default SectionWrapper(GitHubContributions, 'github');
