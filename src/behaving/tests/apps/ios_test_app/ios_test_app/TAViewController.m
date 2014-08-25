//
//  TAViewController.m
//  Behaving Test App
//
//  Created by Erlend Halvorsen on 23/07/14.
//  Copyright (c) 2014 Behaving. All rights reserved.
//

#import "TAViewController.h"

@interface TAViewController () <UIScrollViewDelegate>
@property (weak, nonatomic) IBOutlet UITextField *textField;
@property (weak, nonatomic) IBOutlet UIButton *button;
@property (weak, nonatomic) IBOutlet UISwitch *aSwitch;
@property (weak, nonatomic) IBOutlet UISlider *slider;
@property (weak, nonatomic) IBOutlet UILabel *scrollViewLabel;
@property (weak, nonatomic) IBOutlet UILabel *resultLabel;
@property (weak, nonatomic) IBOutlet UILabel *scrollOffsetLabel;
@property (weak, nonatomic) IBOutlet UIScrollView *scrollView;
@property (weak, nonatomic) IBOutlet UILabel *checked;

@end

@implementation TAViewController

- (void)viewDidLoad
{
    [super viewDidLoad];
    
    self.textField.accessibilityIdentifier = @"textInput";
    self.aSwitch.accessibilityIdentifier = @"toggleCalculate";
    self.slider.accessibilityIdentifier = @"slider";
    self.aSwitch.accessibilityIdentifier = @"switch";
    self.resultLabel.accessibilityIdentifier = @"resultLabel";
    self.scrollView.accessibilityIdentifier = @"scrollView";
    self.scrollViewLabel.accessibilityIdentifier = @"scrollViewLabel";
    self.scrollOffsetLabel.accessibilityIdentifier = @"scrollOffsetLabel";
    self.textField.text = [[NSUserDefaults standardUserDefaults] objectForKey:@"textFieldValue"];
    
    [self scrollViewDidScroll:self.scrollView];
    
    UITapGestureRecognizer* closeKeyboardGesture = [[UITapGestureRecognizer alloc] initWithTarget:self action:@selector(viewTapped:)];
    [self.view addGestureRecognizer:closeKeyboardGesture];
}

- (IBAction)calculate:(id)sender {
    
    self.resultLabel.text = [NSString stringWithFormat:@"%d", self.textField.text.intValue * 2];
}

- (IBAction)resetInput:(id)sender {
    self.button.enabled = self.aSwitch.on;
    self.checked.hidden = !self.aSwitch.on;
}

- (void)viewTapped:(id)sender
{
    [self.view endEditing:YES];
}

- (IBAction)textFieldChanged:(id)sender {
    [[NSUserDefaults standardUserDefaults] setObject:self.textField.text forKey:@"textFieldValue"];
    [[NSUserDefaults standardUserDefaults] synchronize];
}

-(void)scrollViewDidScroll:(UIScrollView *)scrollView
{
    self.scrollOffsetLabel.text = [NSString stringWithFormat:@"%.0f, %.0f", scrollView.contentOffset.x, scrollView.contentOffset.y];
}

@end
