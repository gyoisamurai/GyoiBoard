import Vue from "vue";
import moment from "moment";
import {axios} from "~/plugins/axios";

/* Exchange date format. */
Vue.filter('formatDate', function (value){
  const date = moment(value);
  return date.format("YYYY.MM.DD(ddd) HH:mm");
})

/* Exchange Region. */
Vue.filter('exchangeRegion', function (value) {
  let region = ""
  if (value == 0) {
    region = "-----";
  } else if (value == 1) {
    region = "Domestic";
  } else {
    region = "Abroad";
  }
  return region
})

/* Exchange Industry. */
Vue.filter('exchangeIndustry', function (value) {
  let industry = ""
  if (value == 0) {
    industry = "-----";
  } else if (value == 1) {
    industry = "Energy";
  } else if (value == 2) {
    industry = "Materials";
  } else if (value == 3) {
    industry = "Industrials";
  } else if (value == 4) {
    industry = "Consumer Discretionary";
  } else if (value == 5) {
    industry = "Consumer Staples";
  } else if (value == 6) {
    industry = "Health Care";
  } else if (value == 7) {
    industry = "Financials";
  } else if (value == 8) {
    industry = "Information Technology";
  } else if (value == 9) {
    industry = "Communication Services";
  } else if (value == 10) {
    industry = "Utilities";
  } else {
    industry = "Real Estate";
  }
  return industry
})

/* Exchange Rank. */
Vue.filter('exchangeRank', function (value) {
  let rank = ""
  if (value == 0) {
    rank = "-----";
  } else if (value == 1) {
    rank = "Secure";
  } else if (value == 2) {
    rank = "Normal";
  } else if (value == 3) {
    rank = "Weak";
  } else {
    rank = "Critical";
  }
  return rank
})

/* Exchange Status. */
Vue.filter('exchangeStatus', function (value) {
  let status = ""
  if (value == 0) {
    status = "-----";
  } else if (value == 1) {
    status = "Search";
  } else {
    status = "Assess";
  }
  return status
})

/* Exchange Production. */
Vue.filter('exchangeProduction', function (value) {
  let production = ""
  if (value == 0) {
    production = "-----";
  } else if (value == 1) {
    production = "Development";
  } else {
    production = "Production";
  }
  return production
})

/* Exchange Cloud Type. */
Vue.filter('exchangeCloudType', function (value) {
  let cloud = ""
  if (value == 0) {
    cloud = "-----";
  } else if (value == 1) {
    cloud = "Amazon Web Service";
  } else if (value == 2) {
    cloud = "Google Cloud Platform";
  } else {
    cloud = "Microsoft Azure"
  }
  return cloud
})
