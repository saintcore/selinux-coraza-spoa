# selinux-coraza-spoa

Selinux-policy module for coraza-spoa. Currently the policy is way too generic and needs a lot of adoption / customization. But it allows you to run coraza-spoa ina confined domain with selinux, so still better then nothing. Please also note that the policy rn only allows binding to/from haproxy via http://127.0.0.1:9000 . We will add custom labels etc soon so you can adopt to your needs.

If you didn't got it by now, just to be clear: v1.0.0 is a working release but you should definetly **NOT** use this in production. use at your own risk.