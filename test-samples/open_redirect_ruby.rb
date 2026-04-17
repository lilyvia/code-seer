class OpenRedirectController < ApplicationController
  def vulnerable_redirect_to(user_url)
    redirect_to user_url
  end

  def vulnerable_redirect_back(user_url)
    redirect_back(fallback_location: user_url)
  end

  def vulnerable_sinatra_redirect(user_url)
    redirect user_url
  end
end
