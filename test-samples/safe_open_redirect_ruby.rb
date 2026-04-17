class SafeOpenRedirectController < ApplicationController
  ALLOWED_PATHS = ['/home', '/dashboard'].freeze

  def safe_validate(target)
    ALLOWED_PATHS.include?(target) ? target : '/'
  end

  def safe_redirect_to(user_url)
    redirect_to safe_validate(user_url)
  end

  def safe_hardcoded_redirect
    redirect_to '/dashboard'
  end

  def safe_redirect_back
    redirect_back(fallback_location: '/home')
  end

  def safe_sinatra_redirect
    redirect '/dashboard'
  end
end
