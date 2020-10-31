#include <stdio.h>
#include <openssl/crypto.h>

int main()
{
	printf("Successfully initialized OpenSSL %s\n", OpenSSL_version(OPENSSL_VERSION));
	return 0;
}
