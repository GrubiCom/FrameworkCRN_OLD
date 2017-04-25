/*
 *   GCC116 - Final project of Operating Systems class.
 *   Copyright (C) 2011  Gilson Miranda Júnior, Alexandre Victor Fassio
 *
 *   This program is free software; you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published by
 *   the Free Software Foundation; either version 2 of the License, or
 *   (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU General Public License for more details.
 *
 *   You should have received a copy of the GNU General Public License
 *   along with this program; if not, write to the Free Software
 *   Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
*/

#include <linux/init.h>
#include <linux/module.h>
#include <linux/fs.h>
#include <linux/types.h>	/* size_t */
#include <linux/cdev.h>		/* cdev struct and other functions */
#include <linux/slab.h>		/* kmalloc() & kfree() */
#include <linux/proc_fs.h>	/* to use /proc */
#include <linux/sched.h>	/* current */
#include <asm/uaccess.h>	/* copy_to_user() and copy_from_user() */

#define GCC116_MAJOR 116
#define GCC116_MINOR 1
#define GCC116_NUMOFDEVICES 1

#define GCC116_DEBUG_LEVEL0
#define GCC116_DEBUG_LEVEL1
#define GCC116_DEBUG_LEVEL2

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Gilson Miranda Júnior, Alexandre Victor Fassio");

/** Structures, Types and Function Prototypes **/
/* Buffer structure */
typedef struct bufferType {
	
	unsigned long int size;
	char *data;
	struct bufferType *next;
} buffer_t;

/* cdev structure */
struct cdev *gcc116_cdev;

/* All Function Prototypes */
void gcc116_freemem(buffer_t *);
ssize_t gcc116_read(struct file *, char __user *, size_t, loff_t *);
ssize_t gcc116_write(struct file *, const char __user *, size_t , loff_t *);
static int gcc116_read_procmem(char *, char **, off_t, int, int *, void *);
static int gcc116_setup_cdev(dev_t *);
static int _startup(void);
static void _shutdown(void);

/***** New proc access mode *****/
struct proc_dir_entry *proc_file_entry;

static const struct file_operations proc_file_fops = {
	
	.owner =    THIS_MODULE,
// 	.open  =    gcc116_read_procmem,
	.read  =    gcc116_read,
	.write =    gcc116_write,
};
/********************************/

/* File Operations Structure */
// struct file_operations gcc116_fops = {
// 	.owner =    THIS_MODULE,
// 	.read =     gcc116_read,
// 	.write =    gcc116_write,
// };
/** Structures, Types and Function Prototypes **/

int _gcc116_major = GCC116_MAJOR;
int _gcc116_minor = GCC116_MINOR;
int _gcc116_nr_devs = GCC116_NUMOFDEVICES;

buffer_t *memory_buffer;

void gcc116_freemem(buffer_t *workingBuffer0){
	
	buffer_t *workingBuffer1;
	
	do {
		//if (workingBuffer0 == NULL){
			if( workingBuffer0->next == NULL){
				kfree(workingBuffer0->data);
				kfree(workingBuffer0);
				break;
			}
		//}
		
		workingBuffer1 = workingBuffer0->next;
		
		kfree(workingBuffer0->data);
		kfree(workingBuffer0);
		
		workingBuffer0 = workingBuffer1;

	} while (1);
}

ssize_t gcc116_read(struct file *filp, char __user *buffer, size_t count, loff_t *offp){
	
	ssize_t retval;
	unsigned long int totalSize = 0;
	loff_t startingPosition, newOffp;
	buffer_t *workingBuffer;
	buffer_t *out;
	
	workingBuffer = memory_buffer;
	//if (memory_buffer == NULL){
	//	return 0;
	//}
	
	
	do {
		
		totalSize += workingBuffer->size;
	
		if (workingBuffer->next == NULL){
			break;
		}
		
		workingBuffer = workingBuffer->next;
						
		
	} while (1);
	
	if(*offp >= totalSize){
		gcc116_freemem(memory_buffer);		
		return 0;

	}
	
	workingBuffer = memory_buffer;
	
	startingPosition = workingBuffer->size;
	
	while((*offp >= startingPosition) && (workingBuffer->next != NULL)){
		workingBuffer = workingBuffer->next;
		startingPosition += workingBuffer->size;
	}
	
	newOffp = *offp - (startingPosition - workingBuffer->size);
	
	#ifdef GCC116_DEBUG_LEVEL2
	printk(KERN_INFO "gcc116: reading buffer of %d bytes\n", (workingBuffer->size * sizeof(char)) + sizeof(buffer_t));
	#endif
	
	count = workingBuffer->size - newOffp;
	retval = copy_to_user(buffer, workingBuffer->data + newOffp, count);
	
	*offp += count;
	
	return count;
} 

ssize_t gcc116_write(struct file *filp, const char __user *buffer, size_t count, loff_t *offp){
	
	ssize_t retval;
	buffer_t *workingBuffer;
	
	workingBuffer = memory_buffer;
	
	if(workingBuffer->size != 0){

		while(workingBuffer->next != NULL){
		
			workingBuffer = workingBuffer->next;
		}
	
		workingBuffer->next = kmalloc(sizeof(buffer_t), GFP_KERNEL);
	
		workingBuffer = workingBuffer->next;
	
		if (!workingBuffer) { 
			return -ENOMEM;
		} else {
			memset(workingBuffer, 0, sizeof(buffer_t));
		}
	}
	
	#ifdef GCC116_DEBUG_LEVEL2
	printk(KERN_INFO "gcc116: creating new buffer of %d bytes\n", (count * sizeof(char)) + sizeof(buffer_t));
	#endif
	
	workingBuffer->data = kmalloc(count * sizeof(char), GFP_KERNEL);
	workingBuffer->next = NULL;
	workingBuffer->size = count;

	retval = copy_from_user(workingBuffer->data, buffer, count);
	
	if (retval) {
		return -EFAULT;
	}
	
	*offp += count;

	return count;
}

// static int gcc116_read_procmem(char *page, char **start, off_t offset, int count, int *eof, void *data){
// 	
// 	int len;
// 	unsigned long int totalSize = 0, bufferCount = 0;
// 	buffer_t *workingBuffer;
// 	
// 	workingBuffer = memory_buffer;
// 	
// 	do {
// 		totalSize += workingBuffer->size;
// 		bufferCount++;
// 		
// 		if (workingBuffer->next == NULL){
// 			break;
// 		}
// 		
// 		workingBuffer = workingBuffer->next;
// 		
// 	} while (1);
// 	
// 	len = sprintf(page, "Caracteres armazenados:			%lu\n", totalSize);
// 	len += sprintf(page+len, "Buffers criados:			%lu\n", bufferCount);
// 	len += sprintf(page+len, "Tamanho do buffer vazio:		%lu bytes\n", sizeof(buffer_t));
// 	len += sprintf(page+len, "Tamanho medio de cada buffer:		%lu bytes\n", (sizeof(buffer_t) + (totalSize/bufferCount)));
// 	len += sprintf(page+len, "Memoria total usada por buffers:	%lu bytes\n", ((sizeof(buffer_t)*bufferCount) + totalSize));
// 	len += sprintf(page+len, "Memoria usada pelo modulo:		%u bytes\n", THIS_MODULE->core_size);
// 	len += sprintf(page+len, "Processo em execucao:			\"%s\" (pid %i)\n", current->comm, current->pid);
// 	
// 	return len;
// }

static int gcc116_setup_cdev(dev_t *dev){
	
	if (!(gcc116_cdev = cdev_alloc())){
		return(-1);
	}
	
	gcc116_cdev->owner = THIS_MODULE;
	
	cdev_init(gcc116_cdev, &proc_file_fops);

	if ((cdev_add(gcc116_cdev, *dev, 1)) < 0){
		return(-1);
	}
	
	return(0);
}

static int _startup(void){
	
	/* DEVICE REGISTER */
	int result = 1;
	dev_t dev = 0;
	
	#ifdef GCC116_DEBUG_LEVEL2
	printk(KERN_INFO "gcc116: starting up... Let's Rock 'n Roll!\n");
	#endif
	
	if (_gcc116_major) {
		
		dev = MKDEV(_gcc116_major, _gcc116_minor);
		
		result = register_chrdev_region(dev, _gcc116_nr_devs, "gcc116");
	}
	
	if((_gcc116_major) && (result < 0)){
		
		#ifdef GCC116_DEBUG_LEVEL1
		printk(KERN_WARNING "gcc116: can't get major %d, trying dynamically...\n", _gcc116_major);
		#endif
		
		result = alloc_chrdev_region(&dev, _gcc116_minor, _gcc116_nr_devs, "gcc116");
		
		_gcc116_major = MAJOR(dev);
		_gcc116_minor = MINOR(dev);
	}
	
	if (result < 0) {
		
		printk(KERN_ERR "gcc116: could not register driver %d\n", _gcc116_major);
		return result;
	}
	
	#ifdef GCC116_DEBUG_LEVEL0
	printk(KERN_INFO "gcc116: registered Major=%d Minor=%d\n", _gcc116_major, _gcc116_minor);
	#endif
	/* DEVICE REGISTER */
	
	/* CREATE CDEV */
	if ((gcc116_setup_cdev(&dev)) < 0){

		printk(KERN_ERR "gcc116: failed to allocate or initialize cdev structure... shutting down\n");
		_shutdown();
	}
	/* CREATE CDEV */

	/* CREATE /PROC ENTRY */
// 	create_proc_read_entry("gcc116", 0, NULL, gcc116_read_procmem, NULL);		// DEPRECATED
	proc_file_entry = proc_create("gcc116", 0, NULL, &proc_file_fops);
	/* CREATE /PROC ENTRY */
	
	if(proc_file_entry == NULL){
		
		return -ENOMEM;
	}
	
	/* ALLOC BUFFER */
	memory_buffer = kmalloc(sizeof(buffer_t), GFP_KERNEL);
	
	if (!memory_buffer){
		
		return -ENOMEM;
		
	} else {
		
		memset(memory_buffer, 0, sizeof(buffer_t));
	}
	/* ALLOC BUFFER */
	
	#ifdef GCC116_DEBUG_LEVEL2
	printk(KERN_INFO "gcc116: startup complete! Ready to go...\n");
	#endif
	
	return 0;
}

static void _shutdown(void){
	
	/* DEVICE UNREGISTER */
	dev_t dev = MKDEV(_gcc116_major, _gcc116_minor);
	
	#ifdef GCC116_DEBUG_LEVEL2
	printk(KERN_INFO "gcc116: shutting down...\n");
	#endif

	unregister_chrdev_region(dev, _gcc116_nr_devs);
	
	#ifdef GCC116_DEBUG_LEVEL0
	printk(KERN_INFO "gcc116: unregistered Major=%d Minor=%d\n", _gcc116_major, _gcc116_minor);
	#endif
	/* DEVICE UNREGISTER */
	
	/* DELETE CDEV */
	cdev_del(gcc116_cdev);
	/* DELETE CDEV */
	
	/* DELETE /PROC ENTRY */
	#ifdef GCC116_DEBUG_LEVEL1
	printk(KERN_INFO "gcc116: removing proc entry /proc/gcc116\n");
	#endif
	remove_proc_entry("gcc116", NULL);
	/* DELETE /PROC ENTRY */
	
	#ifdef GCC116_DEBUG_LEVEL2
	printk(KERN_INFO "gcc116: freeing buffers\n");
	#endif
	gcc116_freemem(memory_buffer);
	
	#ifdef GCC116_DEBUG_LEVEL2
	printk(KERN_INFO "gcc116: shutdown complete... bye :)\n");
	#endif
}

module_init(_startup);
module_exit(_shutdown);
