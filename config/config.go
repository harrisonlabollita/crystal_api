package config

type Config struct {
    port int
}

func LoadConfig() *Config {
    return &Config{
        port : 3000,
    }
}
