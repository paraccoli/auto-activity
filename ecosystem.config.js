module.exports = {
  apps: [
    {
      name: 'github-activity-bot',
      script: '/home/paraccoli/apps/auto-activity/run-activity-bot.sh',
      cron_restart: '0 9 * * *', // 毎日9時に実行
      autorestart: false,
      watch: false,
      env: {
        NODE_ENV: 'production'
      }
    },
    {
      name: 'github-auto-pr',
      script: '/home/paraccoli/apps/auto-activity/run-auto-pr.sh',
      cron_restart: '0 10 * * *', // 毎日10時に実行
      autorestart: false,
      watch: false,
      env: {
        NODE_ENV: 'production'
      }
    }
  ]
};