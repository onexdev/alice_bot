# ALICE Bot - Advanced BSC Scanner

![Version](https://img.shields.io/badge/version-1.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)

**ALICE (Advanced Ledger Intelligence Collection Engine)** is a high-performance BSC scanner bot designed for extracting token transfer transaction data from BSCScan with sub-second execution times and professional debugging capabilities.

## 🏗️ Architecture

```
alice_bot/
├── base.py                            # CLI Entry Point & Main Controller
├── core/
│   ├── scanner.py                     # BSC Scanner Core Logic
│   ├── config.py                      # Secure Configuration Manager
│   └── utils.py                       # Utility Functions & Formatters
├── interface/
│   └── terminal.py                    # Professional Terminal Interface
├── credentials/
│   └── bscscan_key.json              # API Key Storage (Secure)
├── result/                           # Output Directory
├── requirements.txt                  # Python Dependencies
└── README.md                         # This Documentation
```

## 🚀 Features

### Core Capabilities

- **Ultra-Fast Execution**: Sub-second transaction processing with optimized algorithms
- **Dual Output Modes**: Full transaction data or wallet addresses only
- **Professional Debugging**: Color-coded terminal output with step-by-step process tracking
- **Critical Error Handling**: Comprehensive error management with detailed solutions
- **Rate Limiting**: Intelligent API rate limiting for optimal performance
- **Data Validation**: Complete input validation and sanitization

### Technical Specifications

- **Execution Time**: < 1 second per API request
- **Rate Limiting**: 5 requests/second (configurable)
- **Error Recovery**: Automatic retry with exponential backoff
- **Memory Optimization**: Efficient data processing for large datasets
- **Security**: Secure credential management and input sanitization

## 📋 Prerequisites

### System Requirements

- Python 3.8+
- Windows/Linux/MacOS
- Internet connection
- BSCScan API key

### Dependencies

```bash
pip install -r requirements.txt
```

## 🔧 Installation

1. **Clone/Download** the project to your desired location:
   
   ```
   C:\Users\xeaon\Pictures\alice_bot\
   ```
1. **Install Dependencies**:
   
   ```bash
   cd alice_bot
   pip install -r requirements.txt
   ```
1. **Configure API Key**:
- The API key is pre-configured in `credentials/bscscan_key.json`
- Modify if needed: `"bscscan_api_key": "YOUR_API_KEY"`
1. **Create Required Directories**:
   
   ```bash
   mkdir result
   ```

## 🎯 Usage

### Command Syntax

```bash
python base.py <command> <wallet_address> <action> <version> <output_file>
```

### Commands

- `sc` | `scan` - Start wallet scanning
- `h` | `help` - Display help information

### Actions

- `p` | `print` - Print results to file

### Versions

- `Vv` - Full version (hash + method + age + from + to + token)
- `Vf` - From version (wallet addresses only)

### Examples

**Full Transaction Data**:

```bash
python base.py sc 0xc51beb5b222aed7f0b56042f04895ee41886b763 p Vv wallet.txt
```

**Wallet Addresses Only**:

```bash
python base.py sc 0xc51beb5b222aed7f0b56042f04895ee41886b763 p Vf wallet.txt
```

**Help**:

```bash
python base.py help
```

## 🔄 Workflow

1. **Initialization**: Bot loads configuration and initializes components
1. **Welcome Screen**: Professional welcome interface with documentation
1. **User Confirmation**: Scan confirmation prompt (y/n)
1. **Data Processing**:
- Wallet validation
- API requests with rate limiting
- Transaction processing
- Data formatting
1. **Output Generation**: Results saved to `result/` directory
1. **Completion Report**: Success confirmation with statistics

## 📊 Output Formats

### Full Version (Vv)

```
Hash: 0x123...abc
Method: transfer
Age: 2 hours ago
From: 0xabc...123
To: 0xdef...456
Token: 1000.000000 USDT (Tether USD)
```

### From Version (Vf)

```
0xabc123def456...
0x789abc012def...
0xfed321cba987...
```

## 🐛 Debugging Features

### Color-Coded Output

- **🔵 BLUE**: Process steps and information
- **🟢 GREEN**: Success messages and confirmations
- **🟡 YELLOW**: Warnings and user prompts
- **🔴 RED**: Errors and critical issues
- **🟣 MAGENTA**: Data output and results
- **🔷 CYAN**: API communications and system info

### Debug Categories

- `[INIT]` - Initialization processes
- `[SCAN]` - Scanning operations
- `[API]` - API communications
- `[PROCESS]` - Data processing
- `[SAVE]` - File operations
- `[ERROR]` - Error handling

## ⚡ Performance Optimization

### Speed Enhancements

- Connection pooling for HTTP requests
- Concurrent processing for large datasets
- Memory-efficient data structures
- Optimized JSON parsing
- Intelligent caching mechanisms

### Rate Limiting Strategy

- Dynamic rate adjustment
- Request queuing system
- Automatic retry logic
- Performance monitoring

## 🛡️ Security Features

### Data Protection

- Secure API key storage
- Input sanitization
- Address validation
- Error message sanitization

### Best Practices

- No hardcoded credentials
- Secure file permissions
- Network timeout protection
- Memory cleanup

## 🔍 Error Handling

### Error Categories

- **NETWORK_ERROR**: Connection issues
- **API_ERROR**: BSCScan API problems
- **TIMEOUT_ERROR**: Request timeouts
- **VALIDATION_ERROR**: Invalid input data
- **FILE_ERROR**: File system issues

### Recovery Mechanisms

- Automatic retry with backoff
- Graceful degradation
- Detailed error reporting
- Solution suggestions

## 📈 API Limitations

### BSCScan API Limits

- **Free Tier**: 5 requests/second
- **Standard**: 10 requests/second
- **Pro**: 20 requests/second

### Optimization Tips

- Use appropriate rate limiting
- Implement request batching
- Cache frequently accessed data
- Monitor API usage

## 🧪 Testing

### Test Cases

1. **Valid Wallet Address**: Standard BSC address
1. **Invalid Address**: Malformed address handling
1. **Empty Results**: Wallets with no transactions
1. **Rate Limiting**: API limit testing
1. **Network Issues**: Connection failure handling

### Performance Benchmarks

- Initialization: < 0.1 seconds
- API Request: < 1.0 seconds
- Data Processing: < 0.5 seconds
- File Writing: < 0.1 seconds

## 🔧 Configuration

### API Configuration (`credentials/bscscan_key.json`)

```json
{
    "bscscan_api_key": "YOUR_API_KEY",
    "rate_limit": 5,
    "timeout": 30,
    "max_retries": 3,
    "base_url": "https://api.bscscan.com/api"
}
```

### Customization Options

- Rate limiting parameters
- Timeout values
- Output formatting
- Debug verbosity levels

## 📝 Changelog

### Version 1.0

- Initial release
- Core scanning functionality
- Professional terminal interface
- Comprehensive error handling
- Full documentation

## 🤝 Contributing

### Development Guidelines

- Follow PEP 8 coding standards
- Implement comprehensive error handling
- Add detailed docstrings
- Include unit tests
- Update documentation

### Code Quality Standards

- Zero tolerance for unhandled exceptions
- Performance optimization mandatory
- Security-first approach
- Professional debugging output

## 📞 Support

### Author Information

- **Developer**: onex_dv
- **GitHub**: https://github.com/onexdev
- **Version**: 1.0 Production Ready

### Getting Help

1. Check this documentation
1. Review error messages and suggestions
1. Verify API key and configuration
1. Test with different wallet addresses
1. Contact support with detailed error logs

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This tool is designed for legitimate blockchain analysis and research purposes. Users are responsible for complying with all applicable laws and regulations. The developers are not responsible for any misuse of this software.

-----

**🎉 Enjoy your blockchain analysis with ALICE Bot!**

*Built with precision engineering and professional standards by onex_dv*
